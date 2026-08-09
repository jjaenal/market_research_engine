"""Out-of-sample testing — chronological train/test split (RSH-003 §6, §7; TODO-025)."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from mre.core.experiment_runner import ExperimentConfig, _exp001_signal_definition, _git_head, compute_report
from mre.core.segments import ensure_normalized, run_on_slice
from mre.loaders.csv_loader import load_dataset
from mre.models.statistics import TradeStatistics


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

    def row(metric: str, value: object) -> str:
        return f"| {metric} | {value} |"

    lines: list[str] = [
        "# EXP-001 Out-of-Sample Testing (TODO-025)",
        "",
        "Methodology: RSH-003 §6/§7 — chronological train/test split,",
        "strategy run unchanged on both segments (frozen EXP-001 config).",
        "Split: first %.1f%% train (in-sample), last %.1f%% test (out-of-sample)."
        % (split_fraction * 100, (1 - split_fraction) * 100),
        "Split point: index %d (%s)." % (result.split_index, result.split_timestamp.isoformat()),
        "Code version: %s" % code_version,
        "Generated on: %s" % generated_on,
        "",
        "## Full-range baseline (context)",
        "",
        "| Metric | Baseline |",
        "| --- | --- |",
        row("Trade count", b.trade_count),
        row("Win rate", "%.4f" % (b.win_rate or 0.0)),
        row("Expectancy", "%.4f" % (b.expectancy or 0.0)),
        row("Profit factor", "%.4f" % (b.profit_factor or 0.0)),
        row("Net P&L", "%.2f" % b.net_pnl),
        row("Max drawdown", "%.2f" % b.max_drawdown),
        "",
        "## In-sample (train) vs out-of-sample (test)",
        "",
        "| Metric | Train | Test | Δ Test/Train |",
        "| --- | --- | --- | --- |",
    ]

    def compare(name: str, train_v: object, test_v: object, fmt: str, delta_fmt: str) -> None:
        lines.append(f"| {name} | {fmt % train_v} | {fmt % test_v} | {delta_fmt} |")

    tr_exp, te_exp = tr.expectancy or 0.0, te.expectancy or 0.0
    tr_pf, te_pf = tr.profit_factor or 0.0, te.profit_factor or 0.0

    compare("Trade count", tr.trade_count, te.trade_count, "%d", "-")
    compare("Win rate", tr.win_rate or 0.0, te.win_rate or 0.0, "%.4f", "-")
    compare("Expectancy", tr_exp, te_exp, "%.4f", "%.1f%%" % (_delta(te_exp, tr_exp) * 100 if _delta(te_exp, tr_exp) is not None else 0.0))
    compare("Profit factor", tr_pf, te_pf, "%.4f", "%.1f%%" % (_delta(te_pf, tr_pf) * 100 if _delta(te_pf, tr_pf) is not None else 0.0))
    compare("Net P&L", tr.net_pnl, te.net_pnl, "%.2f", "%.1f%%" % (_delta(te.net_pnl, tr.net_pnl) * 100 if _delta(te.net_pnl, tr.net_pnl) is not None else 0.0))
    compare("Max drawdown", tr.max_drawdown, te.max_drawdown, "%.2f", "-")
    compare("Sufficient sample", tr.sufficient_sample, te.sufficient_sample, "%s", "-")

    edge_holds = te_exp > 0.0 and te_pf > 1.0 and te.sufficient_sample
    degraded = tr_exp > 0.0 and te_exp < 0.5 * tr_exp

    lines.append("")
    lines.append("## Assessment")
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
    """CLI: run EXP-001 out-of-sample testing and write the markdown report."""
    parser = argparse.ArgumentParser(description="Run EXP-001 out-of-sample testing (TODO-025).")
    parser.add_argument("--out", type=Path, default=Path("experiments/EXP-001/EXP-001_oos.md"))
    parser.add_argument("--split", type=float, default=0.7, help="train fraction (default 0.7)")
    args = parser.parse_args(argv)

    config = _exp001_config(args.out)
    result = run_oos(config, split_fraction=args.split)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        to_markdown(result, config.code_version, config.generated_on, args.split), encoding="utf-8"
    )

    tr, te = result.train, result.test
    print(f"split at index {result.split_index} ({result.split_timestamp.isoformat()})")
    print(f"train: {tr.trade_count} trades, exp {tr.expectancy:.4f}, PF {tr.profit_factor:.4f}")
    print(f"test:  {te.trade_count} trades, exp {te.expectancy:.4f}, PF {te.profit_factor:.4f}")
    print(f"oos report written to {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
