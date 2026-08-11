"""Robustness analysis tests (TODO-026, RSH-003 §10)."""

from __future__ import annotations

import math
from dataclasses import replace
from pathlib import Path

import pytest

from mre.core.experiment_runner import ExperimentConfig
from mre.core.robustness import (
    RobustnessRun,
    _split_cost,
    compute_breakeven,
    run_combo_grid,
    run_cost_grid,
    run_market,
    run_periods,
    run_robustness,
    to_markdown,
)
from mre.models.execution import ExecutionConfig
from mre.loaders.csv_loader import load_dataset
from mre.models.dataset import DataConfig
from mre.models.event import PRICE_CONFIRMATION, RSI_TRENDLINE_BROKEN
from mre.models.signal_rule import SignalRule


def _write_raw(path: Path, n: int = 400, scale: float = 1.0, freq: float = 4.0) -> None:
    lines: list[str] = []
    prev_close = 100.0
    for i in range(n):
        # Alternating smooth-sine / fast-chop segments with rising levels produce
        # EXP-001 signals (see tests/test_out_of_sample.py for the rationale).
        seg = i // 40
        level = float(seg * 4)
        if seg % 2 == 0:
            close = 100.0 + level + math.sin(i / freq) * 3.0 * scale
        else:
            close = 100.0 + level + math.sin(i / 2.0) * 1.0 * scale
        open_ = prev_close
        high = max(open_, close) + 0.5
        low = min(open_, close) - 0.5
        hour = i % 24
        day = 1 + i // 24
        lines.append(
            f"2020-01-{day:02d} {hour:02d}:00,{open_:.3f},{high:.3f},{low:.3f},{close:.3f},10"
        )
        prev_close = close
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _config(tmp_path: Path) -> ExperimentConfig:
    raw = tmp_path / "raw.csv"
    _write_raw(raw)
    return ExperimentConfig(
        experiment_id="EXP-001",
        title="RSI Trendline Breakout Baseline",
        hypothesis="Hipotesis.",
        code_version="test",
        generated_on="2026-08-08",
        strategy={"rsi_period": 14},
        raw_dataset=raw,
        normalized_dataset=tmp_path / "normalized.csv",
        report_path=tmp_path / "report.md",
        signal_definition=(
            SignalRule(
                signal_type="LONG",
                trigger=RSI_TRENDLINE_BROKEN,
                confirmations=(PRICE_CONFIRMATION,),
                window=5,
                source_strategy="rsi_trendline_breakout",
                trigger_payload={"slope__lt": 0.0},
            ),
        ),
    )


def test_periods_split_dataset_chronologically(tmp_path: Path) -> None:
    config = _config(tmp_path)
    runs = run_periods(config, n_periods=4, out_dir=tmp_path)
    assert len(runs) == 4
    assert [r.label for r in runs] == [
        "period-1-of-4",
        "period-2-of-4",
        "period-3-of-4",
        "period-4-of-4",
    ]
    for run in runs:
        assert isinstance(run, RobustnessRun)
        assert (tmp_path / f"XAUUSD_H1_{run.label}.csv").exists()

    data_cfg = config.data_config
    starts: list[Path] = [tmp_path / f"XAUUSD_H1_{r.label}.csv" for r in runs]
    candles = [load_dataset(p, data_cfg).candles for p in starts]
    for k in range(1, len(candles)):
        assert candles[k - 1][-1].timestamp < candles[k][0].timestamp
    total = sum(len(c) for c in candles)
    assert total == 400


def test_periods_requires_positive_count(tmp_path: Path) -> None:
    with pytest.raises(ValueError):
        run_periods(_config(tmp_path), n_periods=0)


def test_cost_grid_control_matches_baseline(tmp_path: Path) -> None:
    result = run_robustness(_config(tmp_path))
    assert result.baseline.trade_count > 0
    assert result.costs[0].label == "comm=0/slip=0"
    assert result.costs[0].statistics == result.baseline


def test_cost_grid_reduces_net_pnl(tmp_path: Path) -> None:
    result = run_robustness(_config(tmp_path))
    assert result.costs[0].statistics.net_pnl > result.costs[-1].statistics.net_pnl


def test_combo_control_matches_baseline(tmp_path: Path) -> None:
    result = run_robustness(_config(tmp_path))
    assert result.combos[0].label == "price_lookback=20/rsi_period=14"
    assert result.combos[0].statistics == result.baseline


def test_market_run_loads_second_symbol(tmp_path: Path) -> None:
    config = _config(tmp_path)
    market_raw = tmp_path / "market_raw.csv"
    _write_raw(market_raw, scale=2.0, freq=3.0)
    run = run_market(config, market_raw, "XAGUSD", out_dir=tmp_path)
    assert run.label == "XAGUSD"
    loaded = load_dataset(tmp_path / "XAGUSD_H1_normalized.csv", DataConfig(symbol="XAGUSD", timeframe="H1"))
    assert loaded.metadata.symbol == "XAGUSD"
    assert loaded.metadata.candle_count == 400


def test_run_robustness_aggregates_all_dimensions(tmp_path: Path) -> None:
    config = _config(tmp_path)
    market_raw = tmp_path / "market_raw.csv"
    _write_raw(market_raw, scale=2.0, freq=3.0)
    result = run_robustness(config, market_csv=market_raw, out_dir=tmp_path)
    assert result.baseline.trade_count > 0
    assert len(result.periods) == 4
    assert len(result.markets) == 1
    assert len(result.costs) == 7
    assert len(result.combos) == 5


def test_split_cost_preserves_frozen_ratio() -> None:
    cfg = ExecutionConfig(commission_rate=0.00003, slippage_rate=0.00007)
    comm, slip = _split_cost(cfg, 2.0)
    assert comm == pytest.approx(0.00006)
    assert slip == pytest.approx(0.00014)
    assert comm + slip == pytest.approx(2.0 * 1e-4)


def test_split_cost_zero_frozen_uses_half() -> None:
    cfg = ExecutionConfig()
    comm, slip = _split_cost(cfg, 2.0)
    assert comm == pytest.approx(1.0 * 1e-4)
    assert slip == pytest.approx(1.0 * 1e-4)


def _flat_config(tmp_path: Path) -> ExperimentConfig:
    raw = tmp_path / "flat_raw.csv"
    _write_raw(raw)
    text = raw.read_text(encoding="utf-8")
    lines = text.splitlines()
    flat_lines: list[str] = []
    for line in lines[:60]:
        parts = line.split(",")
        price = 100.0
        flat_lines.append(f"{parts[0]},{price:.3f},{price:.3f},{price:.3f},{price:.3f},10")
    (tmp_path / "flat.csv").write_text("\n".join(flat_lines) + "\n", encoding="utf-8")
    return replace(
        _config(tmp_path),
        raw_dataset=tmp_path / "flat.csv",
        normalized_dataset=tmp_path / "flat_normalized.csv",
    )


def test_breakeven_positive_for_edge_config(tmp_path: Path) -> None:
    config = _config(tmp_path)
    breakeven = compute_breakeven(config, max_bps=40.0)
    assert breakeven is not None
    assert 0.0 < breakeven < 40.0


def test_breakeven_zero_cost_expectancy_positive(tmp_path: Path) -> None:
    config = _config(tmp_path)
    zero = run_cost_grid(config, grid=((0.0, 0.0),))[0].statistics.expectancy
    assert zero > 0.0
    breakeven = compute_breakeven(config, max_bps=40.0)
    assert breakeven > 0.0


def test_breakeven_none_when_edge_survives_max_cost(tmp_path: Path) -> None:
    config = _config(tmp_path)
    breakeven = compute_breakeven(config, max_bps=1.0)
    assert breakeven is None


def test_breakeven_zero_when_gross_edge_absent(tmp_path: Path) -> None:
    config = _flat_config(tmp_path)
    breakeven = compute_breakeven(config)
    assert breakeven == 0.0


def test_breakeven_monotonic_in_max_bps(tmp_path: Path) -> None:
    config = _config(tmp_path)
    narrow = compute_breakeven(config, max_bps=30.0)
    wide = compute_breakeven(config, max_bps=40.0)
    assert wide is not None
    assert narrow is not None
    assert wide >= narrow
    config = _config(tmp_path)
    market_raw = tmp_path / "market_raw.csv"
    _write_raw(market_raw, scale=2.0, freq=3.0)
    result = run_robustness(config, market_csv=market_raw, out_dir=tmp_path)
    md = to_markdown(result, code_version="abc123", generated_on="2026-08-08")
    assert "Robustness Analysis" in md
    assert "Time Period Stability" in md
    assert "Cross-Market" in md
    assert "Execution Cost & Slippage" in md
    assert "Parameter Combinations" in md
    assert "abc123" in md
    assert "## Assessment" in md
