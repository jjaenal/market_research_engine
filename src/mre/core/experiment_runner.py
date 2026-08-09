"""Experiment runner — CSV → report orchestration (ARC-006 §7, PRD-006 §10)."""

from __future__ import annotations

import subprocess
import sys
from dataclasses import dataclass, field, replace
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

from mre.engines.event_engine import EventEngine, EventEngineConfig
from mre.engines.reporting_engine import render
from mre.engines.signal_engine import combine
from mre.engines.simulation_engine import simulate
from mre.engines.statistics_engine import calculate
from mre.indicators.rsi import rsi
from mre.loaders.csv_loader import load_dataset
from mre.loaders.normalize import RawCsvConfig, normalize_raw_csv
from mre.models.dataset import DataConfig
from mre.models.execution import ExecutionConfig
from mre.models.report import Report, ReportConfig, ReportInput
from mre.models.signal_rule import SignalRule
from mre.models.statistics import StatisticsConfig
from mre.strategies import get as get_strategy


@dataclass(frozen=True)
class IndicatorConfig:
    """Indicator parameters (EXP-001 §9.1)."""

    rsi_period: int = 14


@dataclass(frozen=True)
class ExperimentConfig:
    """Frozen experiment configuration (RSH-002 §9, FR-012)."""

    experiment_id: str
    title: str
    hypothesis: str
    code_version: str
    generated_on: str
    strategy: dict[str, Any] = field(default_factory=dict)
    raw_dataset: Path = Path("datasets/XAUUSD_H1.csv")
    normalized_dataset: Path = Path("experiments/EXP-001/dataset/XAUUSD_H1_normalized.csv")
    report_path: Path = Path("experiments/EXP-001/EXP-001_report.md")
    data_config: DataConfig = field(default_factory=lambda: DataConfig(symbol="XAUUSD", timeframe="H1"))
    indicator_config: IndicatorConfig = field(default_factory=IndicatorConfig)
    event_config: EventEngineConfig = field(default_factory=EventEngineConfig)
    strategy_id: str = ""
    signal_definition: tuple[SignalRule, ...] = ()
    execution_config: ExecutionConfig = field(default_factory=ExecutionConfig)
    statistics_config: StatisticsConfig = field(default_factory=StatisticsConfig)
    conclusion: str = ""

    def __post_init__(self) -> None:
        if not self.experiment_id:
            raise ValueError("experiment_id must not be empty")
        if self.strategy_id and not self.signal_definition:
            object.__setattr__(self, "signal_definition", get_strategy(self.strategy_id))
        if not self.signal_definition:
            raise ValueError("signal_definition must not be empty")


def compute_report(config: ExperimentConfig, dataset_path: Path | None = None) -> Report:
    """Run the pipeline from a normalized CSV to a rendered Report (no file writes).

    Steps (ARC-006 §7): normalize → load → indicators → events →
    signals → simulate → statistics → render. Pure orchestration:
    every stage is deterministic (Article 7) and the dataset is
    immutable (Article 13). The normalized dataset is materialized
    only if ``dataset_path`` does not already exist, so sensitivity
    and robustness runs can reuse one normalized file.
    """
    normalized = dataset_path if dataset_path is not None else config.normalized_dataset
    if not normalized.exists():
        normalize_raw_csv(config.raw_dataset, normalized, RawCsvConfig())

    dataset = load_dataset(normalized, config.data_config)

    closes = [c.close for c in dataset.candles]
    rsi_values = rsi(closes, config.indicator_config.rsi_period)

    events = EventEngine(config.event_config).detect(dataset, {"rsi": rsi_values})
    signals = combine(events, config.signal_definition)
    trades = simulate(signals, dataset.candles, config.execution_config)
    statistics = calculate(trades, config.statistics_config)

    result = ReportInput(
        statistics=statistics,
        trades=trades,
        dataset_metadata=dataset.metadata,
        execution=config.execution_config,
    )
    report = render(
        result,
        ReportConfig(
            experiment_id=config.experiment_id,
            title=config.title,
            hypothesis=config.hypothesis,
            code_version=config.code_version,
            strategy=config.strategy,
            conclusion=config.conclusion,
            generated_on=config.generated_on,
        ),
    )

    return report


def run_experiment(config: ExperimentConfig) -> Report:
    """Run the full pipeline from raw CSV to a rendered Report written to disk."""
    report = compute_report(config)
    config.report_path.parent.mkdir(parents=True, exist_ok=True)
    config.report_path.write_text(report.to_markdown(), encoding="utf-8")
    return report


def _git_head() -> str:
    try:
        out = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            capture_output=True,
            text=True,
            check=True,
        )
        return out.stdout.strip() or "unknown"
    except (subprocess.SubprocessError, FileNotFoundError):
        return "unknown"


def _section(raw: dict[str, Any], name: str) -> dict[str, Any]:
    """Return the named YAML section or fail with a clear message (PRD-003 §7.3)."""
    value = raw.get(name)
    if not isinstance(value, dict):
        raise ValueError(f"missing or invalid '{name}' section in experiment config")
    return value


def _strategy_summary(config: ExperimentConfig) -> dict[str, Any]:
    """Flatten the resolved strategy into the report's Configuration table."""
    rule = config.signal_definition[0]
    payload = " ".join(f"{key} {value}" for key, value in (rule.trigger_payload or {}).items())
    return {
        "rsi_period": config.indicator_config.rsi_period,
        "swing_left": config.event_config.swing_left,
        "swing_right": config.event_config.swing_right,
        "price_lookback": config.event_config.price_lookback,
        "signal_window": rule.window,
        "hold_bars": config.execution_config.hold_bars,
        "trigger_payload": f"{rule.trigger} {payload}".strip(),
    }


def load_experiment_config(path: Path) -> ExperimentConfig:
    """Load a frozen experiment config from a YAML file (FR-012, ARC-008 ARC-ACT-011).

    The YAML is the single source of truth for the experiment parameters
    (RSH-002 §9); run-time concerns (``code_version``, ``generated_on``,
    dataset paths) are filled by the loader, not frozen in the file.
    Rejects invalid YAML and missing sections with clear messages
    (PRD-003 §7.3). The signal definition is resolved from the strategy
    plugin registry by ``strategy_id`` (ARC-ACT-010).
    """
    if not path.exists():
        raise ValueError(f"experiment config file not found: {path}")
    try:
        raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise ValueError(f"invalid YAML in {path}: {exc}") from exc
    if not isinstance(raw, dict):
        raise ValueError(f"experiment config must be a YAML mapping: {path}")

    experiment = _section(raw, "experiment")
    experiment_id = experiment.get("id", "")
    title = experiment.get("title", "")
    hypothesis = experiment.get("hypothesis", "")
    strategy_id = experiment.get("strategy_id", "")

    dataset = _section(raw, "dataset")
    data_config = DataConfig(
        symbol=dataset.get("symbol", "XAUUSD"),
        timeframe=dataset.get("timeframe", "H1"),
        timezone=dataset.get("timezone", "UTC"),
        source=dataset.get("source", "csv"),
    )

    indicator = _section(raw, "indicator")
    indicator_config = IndicatorConfig(rsi_period=int(indicator.get("rsi_period", 14)))

    event = _section(raw, "event")
    event_config = EventEngineConfig(
        swing_left=int(event.get("swing_left", 2)),
        swing_right=int(event.get("swing_right", 2)),
        price_lookback=int(event.get("price_lookback", 20)),
    )

    execution = _section(raw, "execution")
    execution_config = ExecutionConfig(
        position_size=float(execution.get("position_size", 1.0)),
        commission_rate=float(execution.get("commission_rate", 0.0)),
        slippage_rate=float(execution.get("slippage_rate", 0.0)),
        hold_bars=int(execution.get("hold_bars", 10)),
        stop_loss=execution.get("stop_loss"),
        take_profit=execution.get("take_profit"),
    )

    statistics = _section(raw, "statistics")
    statistics_config = StatisticsConfig(min_sample=int(statistics.get("min_sample", 30)))

    paths = _section(raw, "paths")
    config = ExperimentConfig(
        experiment_id=experiment_id,
        title=title,
        hypothesis=hypothesis,
        code_version=_git_head(),
        generated_on=datetime.now(timezone.utc).date().isoformat(),
        raw_dataset=Path(paths.get("raw_dataset", "datasets/XAUUSD_H1.csv")),
        normalized_dataset=Path(paths.get("normalized_dataset", "experiments/EXP-001/dataset/XAUUSD_H1_normalized.csv")),
        report_path=Path(paths.get("report_path", "experiments/EXP-001/EXP-001_report.md")),
        data_config=data_config,
        indicator_config=indicator_config,
        event_config=event_config,
        strategy_id=strategy_id,
        execution_config=execution_config,
        statistics_config=statistics_config,
    )
    return replace(config, strategy=_strategy_summary(config))


DEFAULT_EXPERIMENT_CONFIG = Path("configs/EXP-001.yaml")


def exp001_config(
    out: Path = Path("experiments/EXP-001/EXP-001_report.md"),
    *,
    source: Path = Path("datasets/XAUUSD_H1.csv"),
    config_path: Path = DEFAULT_EXPERIMENT_CONFIG,
) -> ExperimentConfig:
    """Build the frozen EXP-001 config from the external YAML file (ARC-008 ARC-ACT-011).

    The frozen experiment parameters live in ``configs/EXP-001.yaml``
    (single source of truth, RSH-002 §9, FR-012); the CLI only overrides
    the run-time dataset source and report output path. The signal
    definition is resolved from the strategy plugin registry by
    ``strategy_id`` (ARC-ACT-010).
    """
    config = load_experiment_config(config_path)
    return replace(config, raw_dataset=source, report_path=out)


def main(argv: list[str] | None = None) -> int:
    """CLI entry point: run EXP-001 baseline (PRD-006 §8.7)."""
    from mre.cli import main as cli_main

    args = argv if argv is not None else sys.argv[1:]
    return cli_main(["baseline", *args])


if __name__ == "__main__":
    raise SystemExit(main())
