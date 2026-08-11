"""Robustness analysis — stability across data, markets, costs, and parameter combos (RSH-003 §10, TODO-026)."""

from __future__ import annotations

import sys
from dataclasses import dataclass, replace
from pathlib import Path

from mre.core.experiment_runner import ExperimentConfig, compute_report
from mre.core.segments import ensure_normalized, run_on_slice
from mre.loaders.csv_loader import load_dataset
from mre.loaders.normalize import RawCsvConfig, normalize_raw_csv
from mre.models.statistics import TradeStatistics
from mre.utils.markdown import heading, table

# Cost grid (commission_rate, slippage_rate) as fractions of notional per side:
# baseline 0 plus two realistic retail levels for XAUUSD H1 (RSH-003 §10).
COST_GRID: tuple[tuple[float, float], ...] = (
    (0.0, 0.0),
    (0.0002, 0.0),
    (0.0005, 0.0),
    (0.0, 0.0002),
    (0.0, 0.0005),
    (0.0002, 0.0002),
    (0.0005, 0.0005),
)

# Near-baseline (price_lookback, rsi_period) combinations — the two most
# sensitive parameters from sensitivity analysis (EXP-001 §16). The baseline
# pair acts as the determinism control. Descriptive only, not optimization
# (RSH-001 §12).
COMBO_GRID: tuple[tuple[int, int], ...] = (
    (20, 14),
    (10, 7),
    (10, 21),
    (30, 7),
    (30, 21),
)


@dataclass(frozen=True)
class RobustnessRun:
    """One robustness variation with its label and resulting statistics."""

    label: str
    statistics: TradeStatistics


@dataclass(frozen=True)
class RobustnessResult:
    """Baseline plus every robustness dimension (RSH-003 §10)."""

    baseline: TradeStatistics
    periods: tuple[RobustnessRun, ...]
    markets: tuple[RobustnessRun, ...]
    costs: tuple[RobustnessRun, ...]
    combos: tuple[RobustnessRun, ...]


def run_periods(
    config: ExperimentConfig,
    n_periods: int = 4,
    out_dir: Path | None = None,
) -> tuple[RobustnessRun, ...]:
    """Run the frozen config on each of ``n_periods`` equal chronological slices.

    RSH-003 §10 — stability over time ranges: the same strategy and frozen
    config are run unchanged on every contiguous slice of the immutable
    dataset; stable results across slices indicate temporal robustness.
    """
    if n_periods < 1:
        raise ValueError("n_periods must be >= 1")

    normalized = ensure_normalized(config)
    dataset = load_dataset(normalized, config.data_config)
    candles = dataset.candles
    bounds = [round(len(candles) * k / n_periods) for k in range(n_periods + 1)]

    dir_path = out_dir if out_dir is not None else normalized.parent
    runs: list[RobustnessRun] = []
    for k in range(n_periods):
        start, end = bounds[k], bounds[k + 1]
        if end <= start:
            raise ValueError("n_periods too large: produced an empty period")
        label = f"period-{k + 1}-of-{n_periods}"
        segment = run_on_slice(config, candles, start, end, dir_path, label)
        runs.append(RobustnessRun(label=segment.label, statistics=segment.statistics))
    return tuple(runs)


def run_market(
    config: ExperimentConfig,
    raw_csv: Path,
    symbol: str,
    out_dir: Path | None = None,
) -> RobustnessRun:
    """Run the frozen config on a different market (same timeframe).

    RSH-003 §10 — robustness over markets: the strategy parameters were
    pre-registered for the primary market and are applied unchanged to
    ``symbol``. The normalized snapshot for the market is derived from its
    immutable raw CSV (Article 13).
    """
    dir_path = out_dir if out_dir is not None else config.normalized_dataset.parent
    normalized = dir_path / f"{symbol}_H1_normalized.csv"
    normalize_raw_csv(raw_csv, normalized, RawCsvConfig())

    market_config = replace(
        config,
        raw_dataset=raw_csv,
        normalized_dataset=normalized,
        data_config=replace(config.data_config, symbol=symbol),
    )
    statistics = compute_report(market_config, normalized).statistics
    return RobustnessRun(label=symbol, statistics=statistics)


def run_cost_grid(
    config: ExperimentConfig,
    grid: tuple[tuple[float, float], ...] = COST_GRID,
    dataset_path: Path | None = None,
) -> tuple[RobustnessRun, ...]:
    """Run the frozen config under commission/slippage assumptions (RSH-003 §10).

    The first grid entry is the zero-cost baseline control (determinism
    check); later entries model realistic execution costs.
    """
    normalized = dataset_path if dataset_path is not None else ensure_normalized(config)
    runs: list[RobustnessRun] = []
    for commission_rate, slippage_rate in grid:
        variant = replace(
            config,
            execution_config=replace(
                config.execution_config,
                commission_rate=commission_rate,
                slippage_rate=slippage_rate,
            ),
        )
        label = f"comm={commission_rate:g}/slip={slippage_rate:g}"
        runs.append(RobustnessRun(label=label, statistics=compute_report(variant, normalized).statistics))
    return tuple(runs)


def _split_cost(
    exec_config: ExecutionConfig,
    total_bps: float,
) -> tuple[float, float]:
    """Map a total per-side cost (bps) onto commission/slippage rates.

    The frozen config's commission:slippage ratio is scaled
    proportionally so a total-per-side sweep preserves the venue cost
    composition (E-3, SPEC-005). A zero-cost frozen config (EXP-001
    baseline) defaults to a 50/50 split.
    """
    frozen_total = exec_config.commission_rate + exec_config.slippage_rate
    target_total = total_bps * 1e-4
    if frozen_total > 0:
        ratio = target_total / frozen_total
        return exec_config.commission_rate * ratio, exec_config.slippage_rate * ratio
    return target_total * 0.5, target_total * 0.5


def compute_breakeven(
    config: ExperimentConfig,
    dataset_path: Path | None = None,
    *,
    max_bps: float = 20.0,
    tolerance_bps: float = 0.01,
) -> float | None:
    """Compute the per-side cost (bps) at which expectancy crosses zero (E-3).

    The acceptance metric "breakeven >= X bps/side" (EXP-002..008 §13) was
    previously hand-interpolated from printed cost grids; this makes it
    code-executable (SPEC-005, NFR-001). Expectancy is monotonically
    non-increasing in the total per-side cost, so the crossing is found
    by binary search on the frozen commission:slippage ratio
    (``_split_cost``).

    Returns 0.0 when expectancy is non-positive even at zero cost (gross
    edge absent), None when expectancy stays positive through ``max_bps``.
    """
    normalized = dataset_path if dataset_path is not None else ensure_normalized(config)

    def expectancy_at(total_bps: float) -> float:
        commission_rate, slippage_rate = _split_cost(config.execution_config, total_bps)
        variant = replace(
            config,
            execution_config=replace(
                config.execution_config,
                commission_rate=commission_rate,
                slippage_rate=slippage_rate,
            ),
        )
        return compute_report(variant, normalized).statistics.expectancy or 0.0

    if expectancy_at(0.0) <= 0.0:
        return 0.0
    if expectancy_at(max_bps) > 0.0:
        return None

    low, high = 0.0, max_bps
    while high - low > tolerance_bps:
        mid = (low + high) / 2.0
        if expectancy_at(mid) > 0.0:
            low = mid
        else:
            high = mid
    return (low + high) / 2.0


def run_combo_grid(
    config: ExperimentConfig,
    combos: tuple[tuple[int, int], ...] = COMBO_GRID,
    dataset_path: Path | None = None,
) -> tuple[RobustnessRun, ...]:
    """Run the frozen config under near-baseline parameter combinations.

    RSH-003 §10 — stability around the optimum: two parameters vary together
    (sensitivity varies them one at a time, TODO-024). The baseline pair is
    the first entry and acts as the control.
    """
    normalized = dataset_path if dataset_path is not None else ensure_normalized(config)
    runs: list[RobustnessRun] = []
    for price_lookback, rsi_period in combos:
        variant = replace(
            config,
            event_config=replace(config.event_config, price_lookback=price_lookback),
            indicator_config=replace(config.indicator_config, rsi_period=rsi_period),
        )
        label = f"price_lookback={price_lookback}/rsi_period={rsi_period}"
        runs.append(RobustnessRun(label=label, statistics=compute_report(variant, normalized).statistics))
    return tuple(runs)


def run_robustness(
    config: ExperimentConfig,
    n_periods: int = 4,
    market_csv: Path | None = None,
    market_symbol: str = "XAGUSD",
    out_dir: Path | None = None,
) -> RobustnessResult:
    """Run every robustness dimension against the frozen EXP-001 config."""
    normalized = ensure_normalized(config)
    baseline = compute_report(config, normalized).statistics
    periods = run_periods(config, n_periods, out_dir)
    markets = (run_market(config, market_csv, market_symbol, out_dir),) if market_csv is not None else ()
    costs = run_cost_grid(config)
    combos = run_combo_grid(config)
    return RobustnessResult(
        baseline=baseline,
        periods=periods,
        markets=markets,
        costs=costs,
        combos=combos,
    )


_METRIC_HEADERS = ["Variation", "Trades", "Win rate", "Expectancy", "PF", "Net P&L", "Max DD", "Sufficient"]


def _stats_row(label: str, s: TradeStatistics) -> list[object]:
    return [
        label,
        s.trade_count,
        "%.4f" % (s.win_rate or 0.0),
        "%.4f" % (s.expectancy or 0.0),
        "%.4f" % (s.profit_factor or 0.0),
        "%.2f" % s.net_pnl,
        "%.2f" % s.max_drawdown,
        s.sufficient_sample,
    ]


def _metrics_table(lines: list[str], heading_text: str, runs: tuple[RobustnessRun, ...]) -> None:
    lines.extend(
        [
            "",
            heading(2, heading_text),
            "",
            table(_METRIC_HEADERS, [_stats_row(run.label, run.statistics) for run in runs]),
        ]
    )


def _positive(runs: tuple[RobustnessRun, ...]) -> int:
    return sum(1 for r in runs if (r.statistics.expectancy or 0.0) > 0.0 and r.statistics.sufficient_sample)


def to_markdown(
    result: RobustnessResult,
    code_version: str,
    generated_on: str,
) -> str:
    """Render the robustness analysis as markdown (deterministic ordering)."""
    lines: list[str] = [
        heading(1, "EXP-001 Robustness Analysis (TODO-026)"),
        "",
        "Methodology: RSH-003 §10 — stability of the frozen EXP-001 config across",
        "chronological data periods, markets, execution costs, and near-baseline",
        "parameter combinations. Descriptive only; thresholds per RSH-004.",
        "Timeframe dimension (H1) is not varied: only H1 datasets are available.",
        "Code version: %s" % code_version,
        "Generated on: %s" % generated_on,
        "",
        heading(2, "Baseline (EXP-001 frozen config)"),
        "",
        table(
            ["Metric", "Baseline"],
            [
                ["Trade count", result.baseline.trade_count],
                ["Win rate", "%.4f" % (result.baseline.win_rate or 0.0)],
                ["Expectancy", "%.4f" % (result.baseline.expectancy or 0.0)],
                ["Profit factor", "%.4f" % (result.baseline.profit_factor or 0.0)],
                ["Net P&L", "%.2f" % result.baseline.net_pnl],
                ["Max drawdown", "%.2f" % result.baseline.max_drawdown],
                ["Sufficient sample", result.baseline.sufficient_sample],
            ],
        ),
    ]

    _metrics_table(lines, "Time Period Stability (frozen config per chronological slice)", result.periods)
    _metrics_table(lines, "Cross-Market (frozen config, same timeframe)", result.markets)
    _metrics_table(lines, "Execution Cost & Slippage (per-side fraction of notional)", result.costs)
    _metrics_table(lines, "Parameter Combinations (price_lookback / rsi_period)", result.combos)

    pos_periods = _positive(result.periods)
    pos_combos = _positive(result.combos)
    if result.costs:
        highest_cost = result.costs[-1].label
        highest_exp = result.costs[-1].statistics.expectancy or 0.0
    else:
        highest_cost, highest_exp = "baseline", result.baseline.expectancy or 0.0
    market_msg: list[str] = []
    for run in result.markets:
        s = run.statistics
        if s.trade_count == 0:
            market_msg.append(f"- {run.label}: no trades produced on this market (insufficient data for this config).")
        elif (s.expectancy or 0.0) > 0.0 and s.sufficient_sample:
            market_msg.append(f"- {run.label}: positive expectancy reproduced out-of-market.")
        else:
            market_msg.append(f"- {run.label}: edge **not** reproduced (expectancy <= 0 or sample insufficient).")

    lines.extend(
        [
            "",
            "## Assessment",
            "",
            "- Time periods with positive expectancy and sufficient sample: "
            "%d / %d." % (pos_periods, len(result.periods)),
            "- Edge across costs: expectancy at highest modeled cost (%s) is %.4f."
            % (highest_cost, highest_exp),
            "- Parameter combinations with positive expectancy and sufficient sample: "
            "%d / %d (incl. baseline control)." % (pos_combos, len(result.combos)),
        ]
    )
    lines.extend(market_msg)
    lines.append("- Comparison is descriptive; thresholds per RSH-004 are configurable per experiment.")
    lines.append("")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    """CLI: run EXP-001 robustness analysis (PRD-006 §8.7, via ``mre.cli``)."""
    from mre.cli import main as cli_main

    args = argv if argv is not None else sys.argv[1:]
    return cli_main(["robustness", *args])


if __name__ == "__main__":
    raise SystemExit(main())
