"""Out-of-sample testing tests (TODO-025, RSH-003 §6/§7)."""

from __future__ import annotations

import math
from datetime import datetime, timezone
from pathlib import Path

import pytest

from mre.core.experiment_runner import ExperimentConfig
from mre.core.out_of_sample import OosResult, _split_index, run_oos, to_markdown
from mre.loaders.csv_loader import load_dataset
from mre.models.event import PRICE_CONFIRMATION, RSI_TRENDLINE_BROKEN
from mre.models.execution import ExecutionConfig
from mre.models.signal_rule import SignalRule
from mre.models.statistics import TradeStatistics


def _write_raw(path: Path, n: int = 400) -> None:
    lines: list[str] = []
    prev_close = 100.0
    for i in range(n):
        # Alternating smooth-sine / fast-chop segments with rising levels: the
        # smooth stretches form descending RSI swing highs (down-trendlines)
        # and the segment transitions break them, producing EXP-001 signals.
        seg = i // 40
        level = float(seg * 4)
        if seg % 2 == 0:
            close = 100.0 + level + math.sin(i / 4.0) * 3.0
        else:
            close = 100.0 + level + math.sin(i / 2.0) * 1.0
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


def test_split_index_bounds() -> None:
    assert _split_index(1000, 0.7) == 700
    assert _split_index(1000, 0.3) == 300
    with pytest.raises(ValueError):
        _split_index(1000, 0.0)
    with pytest.raises(ValueError):
        _split_index(1000, 1.0)


def test_run_oos_produces_segments(tmp_path: Path) -> None:
    result = run_oos(_config(tmp_path), split_fraction=0.7, out_dir=tmp_path)
    assert (tmp_path / "XAUUSD_H1_train.csv").exists()
    assert (tmp_path / "XAUUSD_H1_test.csv").exists()
    assert isinstance(result, OosResult)
    assert result.baseline.trade_count > 0
    assert result.split_index == 280  # 0.7 * 400
    assert result.split_timestamp == load_dataset(
        tmp_path / "XAUUSD_H1_test.csv", _config(tmp_path).data_config
    ).candles[0].timestamp


def test_segments_are_chronological(tmp_path: Path) -> None:
    result = run_oos(_config(tmp_path), split_fraction=0.7, out_dir=tmp_path)
    train = load_dataset(tmp_path / "XAUUSD_H1_train.csv", _config(tmp_path).data_config)
    test = load_dataset(tmp_path / "XAUUSD_H1_test.csv", _config(tmp_path).data_config)
    assert train.candles[-1].timestamp < test.candles[0].timestamp
    assert result.split_timestamp == test.candles[0].timestamp


def test_run_oos_reuses_normalized_dataset(tmp_path: Path) -> None:
    normalized = tmp_path / "normalized.csv"
    result = run_oos(_config(tmp_path), split_fraction=0.5, out_dir=tmp_path)
    assert normalized.exists()
    assert result.split_index == 200


def test_to_markdown_contains_sections(tmp_path: Path) -> None:
    result = run_oos(_config(tmp_path), split_fraction=0.7, out_dir=tmp_path)
    md = to_markdown(result, code_version="abc123", generated_on="2026-08-08", split_fraction=0.7)
    assert "Out-of-Sample Testing" in md
    assert "In-sample (train) vs out-of-sample (test)" in md
    assert "abc123" in md
    assert "| Trade count |" in md


def test_assessment_flags_degradation() -> None:
    def stats(exp: float, pf: float, n: int = 100) -> TradeStatistics:
        return TradeStatistics(
            trade_count=n, win_count=int(n * 0.5), loss_count=n - int(n * 0.5),
            win_rate=0.5, loss_rate=0.5, avg_win=10.0, avg_loss=10.0,
            risk_reward=1.0, expectancy=exp, profit_factor=pf,
            gross_profit=pf * 500.0, gross_loss=500.0, net_pnl=exp * n,
            max_drawdown=50.0, winning_streak=5, losing_streak=6,
            returns=tuple([0.0] * n), mean_return=0.0, std_return=1.0,
            skewness=0.0, equity_curve=tuple(), sufficient_sample=n >= 30,
        )

    strong = OosResult(baseline=stats(1.0, 1.2), train=stats(2.0, 1.4), test=stats(0.6, 1.1),
                       split_index=700, split_timestamp=datetime(2020, 1, 1, tzinfo=timezone.utc))
    md = to_markdown(strong, "abc", "2026-08-08", 0.7)
    assert "Edge remains positive out-of-sample" in md
    assert "Large degradation" in md  # 0.6 < 0.5 * 2.0

    broken = OosResult(baseline=stats(1.0, 1.2), train=stats(2.0, 1.4), test=stats(-0.5, 0.8),
                       split_index=700, split_timestamp=datetime(2020, 1, 1, tzinfo=timezone.utc))
    md = to_markdown(broken, "abc", "2026-08-08", 0.7)
    assert "Edge not reproduced out-of-sample" in md

    stable = OosResult(baseline=stats(1.0, 1.2), train=stats(2.0, 1.4), test=stats(1.8, 1.3),
                       split_index=700, split_timestamp=datetime(2020, 1, 1, tzinfo=timezone.utc))
    md = to_markdown(stable, "abc", "2026-08-08", 0.7)
    assert "Edge remains positive out-of-sample" in md
    assert "No large in-sample → OOS expectancy degradation" in md
