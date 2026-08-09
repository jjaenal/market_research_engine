"""Out-of-sample testing — chronological train/test split (RSH-003 §6, §7; TODO-025)."""

from __future__ import annotations

import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from mre.core.experiment_runner import ExperimentConfig, compute_report
from mre.core.segments import ensure_normalized, run_on_slice
from mre.loaders.csv_loader import load_dataset
from mre.models.statistics import TradeStatistics
from mre.utils.markdown import heading, table


@dataclass(frozen=True)
class OosResult:
    """Full-range baseline plus train (in-sample) and test (out-of-sample) statistics."""

    baseline: TradeStatistics
    train: TradeStatistics
    test: TradeStatistics
    split_index: int
    split_timestamp: datetime


def _split_index(candle_count: int, split_fraction: float) -> int:
    if not 0.0 < split_fraction < 1.0:
        raise ValueError("split_fraction must be in (0, 1)")
    return int(round(candle_count * split_fraction))


def run_oos(
    config: ExperimentConfig,
    split_fraction: float = 0.7,
    out_dir: Path | None = None,
) -> OosResult:
    """Split the immutable dataset chronologically and run the frozen config on each segment.

    RSH-003 §6: no leakage, no retroactive allocation. RSH-003 §7: the
    strategy (EXP-001 frozen config) is run unchanged on the unseen
    test portion; the split point is recorded for the record.
    """
    normalized = ensure_normalized(config)

    dataset = load_dataset(normalized, config.data_config)
    candles = dataset.candles
    idx = _split_index(len(candles), split_fraction)

    dir_path = out_dir if out_dir is not None else normalized.parent
    train = run_on_slice(config, candles, 0, idx, dir_path, "train")
    test = run_on_slice(config, candles, idx, len(candles), dir_path, "test")

    baseline = compute_report(config, normalized).statistics

    return OosResult(
        baseline=baseline,
        train=train.statistics,
        test=test.statistics,
        split_index=idx,
        split_timestamp=candles[idx].timestamp,
    )


def _delta(actual: float | None, reference: float | None) -> float | None:
    if actual is None or reference is None or reference == 0.0:
        return None
    return (actual - reference) / reference


def to_markdown(
    result: OosResult,
    code_version: str,
    generated_on: str,
    split_fraction: float,
) -> str:
    """Render train/test comparison as markdown (deterministic ordering)."""
    b, tr, te = result.baseline, result.train, result.test

    lines: list[str] = [
        heading(1, "EXP-001 Out-of-Sample Testing (TODO-025)"),
        "",
        "Methodology: RSH-003 §6/§7 — chronological train/test split,",
        "strategy run unchanged on both segments (frozen EXP-001 config).",
        "Split: first %.1f%% train (in-sample), last %.1f%% test (out-of-sample)."
        % (split_fraction * 100, (1 - split_fraction) * 100),
        "Split point: index %d (%s)." % (result.split_index, result.split_timestamp.isoformat()),
        "Code version: %s" % code_version,
        "Generated on: %s" % generated_on,
        "",
        heading(2, "Full-range baseline (context)"),
        "",
        table(
            ["Metric", "Baseline"],
            [
                ["Trade count", b.trade_count],
                ["Win rate", "%.4f" % (b.win_rate or 0.0)],
                ["Expectancy", "%.4f" % (b.expectancy or 0.0)],
                ["Profit factor", "%.4f" % (b.profit_factor or 0.0)],
                ["Net P&L", "%.2f" % b.net_pnl],
                ["Max drawdown", "%.2f" % b.max_drawdown],
            ],
        ),
        "",
        heading(2, "In-sample (train) vs out-of-sample (test)"),
        "",
    ]

    tr_exp, te_exp = tr.expectancy or 0.0, te.expectancy or 0.0
    tr_pf, te_pf = tr.profit_factor or 0.0, te.profit_factor or 0.0

    def fmt_delta(actual: float | None, reference: float | None) -> str:
        d = _delta(actual, reference)
        return "-" if d is None else "%.1f%%" % (d * 100)

    lines.append(
        table(
            ["Metric", "Train", "Test", "Δ Test/Train"],
            [
                ["Trade count", tr.trade_count, te.trade_count, "-"],
                ["Win rate", "%.4f" % (tr.win_rate or 0.0), "%.4f" % (te.win_rate or 0.0), "-"],
                ["Expectancy", "%.4f" % tr_exp, "%.4f" % te_exp, fmt_delta(te_exp, tr_exp)],
                ["Profit factor", "%.4f" % tr_pf, "%.4f" % te_pf, fmt_delta(te_pf, tr_pf)],
                ["Net P&L", "%.2f" % tr.net_pnl, "%.2f" % te.net_pnl, fmt_delta(te.net_pnl, tr.net_pnl)],
                ["Max drawdown", "%.2f" % tr.max_drawdown, "%.2f" % te.max_drawdown, "-"],
                ["Sufficient sample", tr.sufficient_sample, te.sufficient_sample, "-"],
            ],
        )
    )

    edge_holds = te_exp > 0.0 and te_pf > 1.0 and te.sufficient_sample
    degraded = tr_exp > 0.0 and te_exp < 0.5 * tr_exp

    lines.append("")
    lines.append(heading(2, "Assessment"))
    lines.append("")
    if edge_holds:
        lines.append("- Edge remains positive out-of-sample (expectancy > 0, PF > 1, sample sufficient).")
    else:
        lines.append("- **Edge not reproduced out-of-sample** (expectancy <= 0 or PF <= 1 or sample insufficient).")
    if degraded:
        lines.append("- **Large degradation** in-sample → OOS expectancy (>= 50% loss): overfitting indicator (RSH-003 §7).")
    else:
        lines.append("- No large in-sample → OOS expectancy degradation.")
    lines.append("- Comparison is descriptive; thresholds per RSH-004 are configurable per experiment.")
    lines.append("")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    """CLI: run EXP-001 out-of-sample testing (PRD-006 §8.7, via ``mre.cli``)."""
    from mre.cli import main as cli_main

    args = argv if argv is not None else sys.argv[1:]
    return cli_main(["oos", *args])


if __name__ == "__main__":
    raise SystemExit(main())
