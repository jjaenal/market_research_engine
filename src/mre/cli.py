"""Unified experiment CLI — one entrypoint with subcommands (ARC-008 ARC-ACT-014)."""

from __future__ import annotations

import argparse
from pathlib import Path

from mre.core.experiment_runner import exp001_config, run_experiment
from mre.core.out_of_sample import run_oos, to_markdown as oos_to_markdown
from mre.core.robustness import run_robustness, to_markdown as robustness_to_markdown
from mre.core.sensitivity import EXP001_GRID, run_sensitivity, to_markdown as sensitivity_to_markdown


def _cmd_baseline(args: argparse.Namespace) -> int:
    config = exp001_config(
        args.out,
        source=args.source,
        experiment_id=args.experiment_id,
        title=args.title,
        hypothesis=args.hypothesis,
    )
    report = run_experiment(config)
    print(f"experiment {report.experiment_id}: {report.statistics.trade_count} trades, "
          f"net P&L {report.statistics.net_pnl:g}, win rate {report.statistics.win_rate or 0.0:.4f}")
    print(f"report written to {config.report_path}")
    return 0


def _cmd_sensitivity(args: argparse.Namespace) -> int:
    config = exp001_config(args.out, source=args.source)
    result = run_sensitivity(config, EXP001_GRID)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        sensitivity_to_markdown(result, config.code_version, config.generated_on, config.strategy),
        encoding="utf-8",
    )

    b = result.baseline
    print(f"baseline: {b.trade_count} trades, expectancy {b.expectancy or 0.0:.4f}, PF {b.profit_factor or 0.0:.4f}")
    for parameter in ("rsi_period", "price_lookback", "signal_window", "hold_bars"):
        runs = result.for_parameter(parameter)
        print(f"{parameter}: " + ", ".join(f"{r.value}->exp {r.statistics.expectancy or 0.0:.4f}" for r in runs))
    print(f"sensitivity report written to {args.out}")
    return 0


def _cmd_oos(args: argparse.Namespace) -> int:
    config = exp001_config(args.out, source=args.source)
    result = run_oos(config, split_fraction=args.split)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        oos_to_markdown(result, config.code_version, config.generated_on, args.split), encoding="utf-8"
    )

    tr, te = result.train, result.test
    print(f"split at index {result.split_index} ({result.split_timestamp.isoformat()})")
    print(f"train: {tr.trade_count} trades, exp {tr.expectancy or 0.0:.4f}, PF {tr.profit_factor or 0.0:.4f}")
    print(f"test:  {te.trade_count} trades, exp {te.expectancy or 0.0:.4f}, PF {te.profit_factor or 0.0:.4f}")
    print(f"oos report written to {args.out}")
    return 0


def _cmd_robustness(args: argparse.Namespace) -> int:
    config = exp001_config(args.out, source=args.source)
    out_dir = config.normalized_dataset.parent
    market_csv = None if args.no_market else args.market
    result = run_robustness(config, n_periods=args.periods, market_csv=market_csv, out_dir=out_dir)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(robustness_to_markdown(result, config.code_version, config.generated_on), encoding="utf-8")

    b = result.baseline
    print(f"baseline: {b.trade_count} trades, expectancy {b.expectancy or 0.0:.4f}, PF {b.profit_factor or 0.0:.4f}")
    for run in result.periods:
        s = run.statistics
        print(f"{run.label}: {s.trade_count} trades, exp {s.expectancy or 0.0:.4f}, PF {s.profit_factor or 0.0:.4f}")
    for run in result.markets:
        s = run.statistics
        print(f"market {run.label}: {s.trade_count} trades, exp {s.expectancy or 0.0:.4f}, PF {s.profit_factor or 0.0:.4f}")
    last = result.costs[-1].statistics
    print(f"highest cost ({result.costs[-1].label}): exp {last.expectancy or 0.0:.4f}, PF {last.profit_factor or 0.0:.4f}")
    print(f"robustness report written to {args.out}")
    return 0


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="MRE experiment CLI (CSV → report).")
    sub = parser.add_subparsers(dest="command", required=True)

    baseline = sub.add_parser("baseline", help="run EXP-001 baseline report")
    baseline.add_argument("--source", type=Path, default=Path("datasets/XAUUSD_H1.csv"))
    baseline.add_argument("--experiment-id", default="EXP-001")
    baseline.add_argument("--title", default="RSI Trendline Breakout Baseline")
    baseline.add_argument(
        "--hypothesis",
        default="Breakout RSI trendline yang dikonfirmasi harga pada XAUUSD H1 "
        "menghasilkan expectancy positif setelah biaya transaksi.",
    )
    baseline.add_argument("--out", type=Path, default=Path("experiments/EXP-001/EXP-001_report.md"))
    baseline.set_defaults(handler=_cmd_baseline)

    sensitivity = sub.add_parser("sensitivity", help="run EXP-001 sensitivity analysis")
    sensitivity.add_argument("--source", type=Path, default=Path("datasets/XAUUSD_H1.csv"))
    sensitivity.add_argument("--out", type=Path, default=Path("experiments/EXP-001/EXP-001_sensitivity.md"))
    sensitivity.set_defaults(handler=_cmd_sensitivity)

    oos = sub.add_parser("oos", help="run EXP-001 out-of-sample testing")
    oos.add_argument("--source", type=Path, default=Path("datasets/XAUUSD_H1.csv"))
    oos.add_argument("--out", type=Path, default=Path("experiments/EXP-001/EXP-001_oos.md"))
    oos.add_argument("--split", type=float, default=0.7, help="train fraction (default 0.7)")
    oos.set_defaults(handler=_cmd_oos)

    robustness = sub.add_parser("robustness", help="run EXP-001 robustness analysis")
    robustness.add_argument("--source", type=Path, default=Path("datasets/XAUUSD_H1.csv"))
    robustness.add_argument("--out", type=Path, default=Path("experiments/EXP-001/EXP-001_robustness.md"))
    robustness.add_argument("--periods", type=int, default=4, help="number of chronological slices (default 4)")
    robustness.add_argument(
        "--market",
        type=Path,
        default=Path("datasets/XAGUSD_H1.csv"),
        help="second market raw CSV to test cross-market robustness",
    )
    robustness.add_argument("--no-market", action="store_true", help="skip the cross-market dimension")
    robustness.set_defaults(handler=_cmd_robustness)

    return parser


def main(argv: list[str] | None = None) -> int:
    """Run the requested experiment subcommand (PRD-006 §8.7)."""
    parser = _build_parser()
    args = parser.parse_args(argv)
    return args.handler(args)


if __name__ == "__main__":
    raise SystemExit(main())
