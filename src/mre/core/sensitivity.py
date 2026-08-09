"""Sensitivity analysis — one-parameter-at-a-time validation (RSH-003 §9, TODO-024)."""

from __future__ import annotations

import sys
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Any, Mapping, Sequence

from mre.core.experiment_runner import ExperimentConfig, compute_report
from mre.models.statistics import TradeStatistics
from mre.utils.markdown import heading, table

# EXP-001 sensitivity grid (RSH-003 §9): one parameter varied, others at baseline.
# Baseline values are included as control runs (determinism check).
EXP001_GRID: dict[str, Sequence[float]] = {
    "rsi_period": (7, 14, 21),
    "price_lookback": (10, 20, 30),
    "signal_window": (3, 5, 10),
    "hold_bars": (5, 10, 20),
    "swing_left": (1, 2, 3),
    "swing_right": (1, 2, 3),
}


@dataclass(frozen=True)
class SensitivityRun:
    """One parameter variation with its resulting statistics."""

    parameter: str
    value: float
    statistics: TradeStatistics


@dataclass(frozen=True)
class SensitivityResult:
    """Baseline statistics plus every one-parameter variation."""

    baseline: TradeStatistics
    runs: tuple[SensitivityRun, ...]

    def for_parameter(self, parameter: str) -> tuple[SensitivityRun, ...]:
        """Runs that vary ``parameter`` (control run included)."""
        return tuple(r for r in self.runs if r.parameter == parameter)


def _vary(config: ExperimentConfig, parameter: str, value: float) -> ExperimentConfig:
    """Return ``config`` with exactly one parameter replaced (control holds)."""
    if parameter == "rsi_period":
        return replace(config, indicator_config=replace(config.indicator_config, rsi_period=int(value)))
    if parameter == "swing_left":
        return replace(config, event_config=replace(config.event_config, swing_left=int(value)))
    if parameter == "swing_right":
        return replace(config, event_config=replace(config.event_config, swing_right=int(value)))
    if parameter == "price_lookback":
        return replace(config, event_config=replace(config.event_config, price_lookback=int(value)))
    if parameter == "signal_window":
        rules = tuple(replace(r, window=int(value)) for r in config.signal_definition)
        return replace(config, signal_definition=rules)
    if parameter == "hold_bars":
        return replace(config, execution_config=replace(config.execution_config, hold_bars=int(value)))
    raise ValueError(f"unknown sensitivity parameter: {parameter}")


def run_sensitivity(
    config: ExperimentConfig,
    grid: Mapping[str, Sequence[float]],
    dataset_path: Path | None = None,
) -> SensitivityResult:
    """Run the baseline plus every one-parameter variation (RSH-003 §9).

    The normalized dataset is materialized once and reused across runs
    so every variation shares the same immutable input (Article 13).
    """
    normalized = dataset_path if dataset_path is not None else config.normalized_dataset
    baseline = compute_report(config, normalized).statistics

    runs: list[SensitivityRun] = []
    for parameter, values in grid.items():
        for value in values:
            stats = compute_report(_vary(config, parameter, value), normalized).statistics
            runs.append(SensitivityRun(parameter=parameter, value=value, statistics=stats))
    return SensitivityResult(baseline=baseline, runs=tuple(runs))


def to_markdown(
    result: SensitivityResult,
    code_version: str,
    generated_on: str,
    strategy: dict[str, Any],
) -> str:
    """Render the sensitivity table as markdown (deterministic ordering)."""
    lines: list[str] = [
        heading(1, "EXP-001 Sensitivity Analysis (TODO-024)"),
        "",
        "Methodology: RSH-003 §9 — one parameter varied, others fixed (control).",
        "Code version: %s" % code_version,
        "Generated on: %s" % generated_on,
        "",
        heading(2, "Baseline (EXP-001 frozen config)"),
        "",
    ]
    b = result.baseline
    lines.append(
        table(
            ["Metric", "Baseline"],
            [
                ["Trade count", b.trade_count],
                ["Win rate", "%.4f" % (b.win_rate or 0.0)],
                ["Expectancy", "%.4f" % (b.expectancy or 0.0)],
                ["Profit factor", "%.4f" % (b.profit_factor or 0.0)],
                ["Net P&L", "%.2f" % b.net_pnl],
                ["Max drawdown", "%.2f" % b.max_drawdown],
                ["Sufficient sample", b.sufficient_sample],
            ],
        )
    )

    parameters = tuple(dict.fromkeys(r.parameter for r in result.runs))
    for parameter in parameters:
        rows: list[list[object]] = []
        for run in result.for_parameter(parameter):
            s = run.statistics
            rows.append(
                [
                    run.value,
                    s.trade_count,
                    "%.4f" % (s.win_rate or 0.0),
                    "%.4f" % (s.expectancy or 0.0),
                    "%.4f" % (s.profit_factor or 0.0),
                    "%.2f" % s.net_pnl,
                    "%.2f" % s.max_drawdown,
                    s.sufficient_sample,
                ]
            )
        lines.extend(
            [
                "",
                heading(2, "Parameter: %s" % parameter),
                "",
                table(
                    ["Value", "Trades", "Win rate", "Expectancy", "PF", "Net P&L", "Max DD", "Sufficient"],
                    rows,
                ),
            ]
        )
    lines.append("")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    """CLI: run EXP-001 sensitivity analysis (PRD-006 §8.7, via ``mre.cli``)."""
    from mre.cli import main as cli_main

    args = argv if argv is not None else sys.argv[1:]
    return cli_main(["sensitivity", *args])


if __name__ == "__main__":
    raise SystemExit(main())
