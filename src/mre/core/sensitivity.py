"""Sensitivity analysis — one-parameter-at-a-time validation (RSH-003 §9, TODO-024)."""

from __future__ import annotations

import argparse
from dataclasses import dataclass, replace
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping, Sequence

from mre.core.experiment_runner import ExperimentConfig, _exp001_signal_definition, _git_head, compute_report
from mre.models.statistics import TradeStatistics

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
        "# EXP-001 Sensitivity Analysis (TODO-024)",
        "",
        "Methodology: RSH-003 §9 — one parameter varied, others fixed (control).",
        "Code version: %s" % code_version,
        "Generated on: %s" % generated_on,
        "",
        "## Baseline (EXP-001 frozen config)",
        "",
    ]
    b = result.baseline
    lines.append(
        "| Metric | Baseline |"
        "\n| --- | --- |"
        "\n| Trade count | %d |"
        "\n| Win rate | %.4f |"
        "\n| Expectancy | %.4f |"
        "\n| Profit factor | %.4f |"
        "\n| Net P&L | %.2f |"
        "\n| Max drawdown | %.2f |"
        "\n| Sufficient sample | %s |"
        "\n" % (b.trade_count, b.win_rate or 0.0, b.expectancy or 0.0,
                b.profit_factor or 0.0, b.net_pnl, b.max_drawdown, b.sufficient_sample)
    )

    parameters = tuple(dict.fromkeys(r.parameter for r in result.runs))
    for parameter in parameters:
        lines.extend(
            [
                "",
                "## Parameter: %s" % parameter,
                "",
                "| Value | Trades | Win rate | Expectancy | PF | Net P&L | Max DD | Sufficient |",
                "| --- | --- | --- | --- | --- | --- | --- | --- |",
            ]
        )
        for run in result.for_parameter(parameter):
            s = run.statistics
            lines.append(
                "| %s | %d | %.4f | %.4f | %.4f | %.2f | %.2f | %s |"
                % (run.value, s.trade_count, s.win_rate or 0.0, s.expectancy or 0.0,
                   s.profit_factor or 0.0, s.net_pnl, s.max_drawdown, s.sufficient_sample)
            )
    lines.append("")
    return "\n".join(lines)


def _exp001_config(out: Path) -> ExperimentConfig:
    return ExperimentConfig(
        experiment_id="EXP-001",
        title="RSI Trendline Breakout Baseline",
        hypothesis="Breakout RSI trendline yang dikonfirmasi harga pada XAUUSD H1 "
        "menghasilkan expectancy positif setelah biaya transaksi.",
        code_version=_git_head(),
        generated_on=datetime.now(timezone.utc).date().isoformat(),
        strategy={
            "rsi_period": 14,
            "swing_left": 2,
            "swing_right": 2,
            "price_lookback": 20,
            "signal_window": 5,
            "hold_bars": 10,
            "trigger_payload": "RSI_TRENDLINE_BROKEN slope__lt 0.0",
        },
        report_path=out,
        signal_definition=_exp001_signal_definition(),
    )


def main(argv: list[str] | None = None) -> int:
    """CLI: run EXP-001 sensitivity analysis and write the markdown report."""
    parser = argparse.ArgumentParser(description="Run EXP-001 sensitivity analysis (TODO-024).")
    parser.add_argument("--out", type=Path, default=Path("experiments/EXP-001/EXP-001_sensitivity.md"))
    args = parser.parse_args(argv)

    config = _exp001_config(args.out)
    result = run_sensitivity(config, EXP001_GRID)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(to_markdown(result, config.code_version, config.generated_on, config.strategy), encoding="utf-8")

    b = result.baseline
    print(f"baseline: {b.trade_count} trades, expectancy {b.expectancy:.4f}, PF {b.profit_factor:.4f}")
    for parameter in ("rsi_period", "price_lookback", "signal_window", "hold_bars"):
        runs = result.for_parameter(parameter)
        print(f"{parameter}: " + ", ".join(f"{r.value}->exp {r.statistics.expectancy:.4f}" for r in runs))
    print(f"sensitivity report written to {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
