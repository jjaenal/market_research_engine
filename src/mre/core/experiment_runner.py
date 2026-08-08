"""Experiment runner — CSV → report orchestration (ARC-006 §7, PRD-006 §10)."""

from __future__ import annotations

import argparse
import subprocess
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from mre.engines.event_engine import EventEngine, EventEngineConfig
from mre.engines.reporting_engine import render
from mre.engines.signal_engine import combine
from mre.engines.simulation_engine import simulate
from mre.engines.statistics_engine import calculate
from mre.indicators.rsi import rsi
from mre.loaders.csv_loader import load_dataset
from mre.loaders.normalize import RawCsvConfig, normalize_raw_csv
from mre.models.dataset import DataConfig
from mre.models.event import PRICE_CONFIRMATION, RSI_TRENDLINE_BROKEN
from mre.models.execution import ExecutionConfig
from mre.models.report import Report, ReportConfig, ReportInput
from mre.models.signal_rule import SignalRule
from mre.models.statistics import StatisticsConfig


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
    signal_definition: tuple[SignalRule, ...] = ()
    execution_config: ExecutionConfig = field(default_factory=ExecutionConfig)
    statistics_config: StatisticsConfig = field(default_factory=StatisticsConfig)
    conclusion: str = ""

    def __post_init__(self) -> None:
        if not self.experiment_id:
            raise ValueError("experiment_id must not be empty")
        if not self.signal_definition:
            raise ValueError("signal_definition must not be empty")


def run_experiment(config: ExperimentConfig) -> Report:
    """Run the full pipeline from raw CSV to a rendered Report.

    Steps (ARC-006 §7): normalize → load → indicators → events →
    signals → simulate → statistics → render. Pure orchestration:
    every stage is deterministic (Article 7) and the dataset is
    immutable (Article 13).
    """
    normalize_raw_csv(config.raw_dataset, config.normalized_dataset, RawCsvConfig())

    dataset = load_dataset(config.normalized_dataset, config.data_config)

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


def _exp001_signal_definition() -> tuple[SignalRule, ...]:
    """EXP-001 §9.3 signal definition (LONG baseline, ENG-003 §10)."""
    return (
        SignalRule(
            signal_type="LONG",
            trigger=RSI_TRENDLINE_BROKEN,
            confirmations=(PRICE_CONFIRMATION,),
            window=5,
            source_strategy="rsi_trendline_breakout",
            trigger_payload={"slope__lt": 0.0},
        ),
    )


def main(argv: list[str] | None = None) -> int:
    """CLI entry point: run EXP-001 baseline (PRD-006 §8.7)."""
    parser = argparse.ArgumentParser(description="Run an MRE experiment (CSV → report).")
    parser.add_argument("--source", type=Path, default=Path("datasets/XAUUSD_H1.csv"))
    parser.add_argument("--experiment-id", default="EXP-001")
    parser.add_argument("--title", default="RSI Trendline Breakout Baseline")
    parser.add_argument(
        "--hypothesis",
        default="Breakout RSI trendline yang dikonfirmasi harga pada XAUUSD H1 "
        "menghasilkan expectancy positif setelah biaya transaksi.",
    )
    parser.add_argument("--out", type=Path, default=Path("experiments/EXP-001/EXP-001_report.md"))
    args = parser.parse_args(argv)

    config = ExperimentConfig(
        experiment_id=args.experiment_id,
        title=args.title,
        hypothesis=args.hypothesis,
        code_version=_git_head(),
        generated_on=datetime.now(timezone.utc).date().isoformat(),
        strategy={
            "rsi_period": 14,
            "swing_left": 2,
            "swing_right": 2,
            "price_lookback": 20,
            "signal_window": 5,
            "trigger_payload": "RSI_TRENDLINE_BROKEN slope__lt 0.0",
        },
        raw_dataset=args.source,
        report_path=args.out,
        signal_definition=_exp001_signal_definition(),
    )

    report = run_experiment(config)
    print(f"experiment {report.experiment_id}: {report.statistics.trade_count} trades, "
          f"net P&L {report.statistics.net_pnl:g}, win rate {report.statistics.win_rate}")
    print(f"report written to {config.report_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
