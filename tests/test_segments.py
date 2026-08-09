"""Shared segment runner tests (ARC-008 ARC-ACT-013)."""

from __future__ import annotations

import math
from pathlib import Path

import pytest

from mre.core.experiment_runner import ExperimentConfig
from mre.core.segments import SegmentRun, ensure_normalized, run_on_slice
from mre.loaders.csv_loader import load_dataset
from mre.models.event import PRICE_CONFIRMATION, RSI_TRENDLINE_BROKEN
from mre.models.signal_rule import SignalRule


def _write_raw(path: Path, n: int = 400) -> None:
    lines: list[str] = []
    prev_close = 100.0
    for i in range(n):
        # Same synthetic pattern as test_out_of_sample/test_robustness:
        # alternating smooth-sine / fast-chop with rising levels produces
        # EXP-001 signals.
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


def test_ensure_normalized_materializes_snapshot(tmp_path: Path) -> None:
    config = _config(tmp_path)
    assert not config.normalized_dataset.exists()
    assert ensure_normalized(config) == config.normalized_dataset
    assert config.normalized_dataset.exists()


def test_ensure_normalized_is_idempotent(tmp_path: Path) -> None:
    config = _config(tmp_path)
    first = ensure_normalized(config)
    second = ensure_normalized(config)
    assert first == second
    assert load_dataset(first, config.data_config).metadata.candle_count == 400


def test_run_on_slice_writes_labeled_csv_and_runs(tmp_path: Path) -> None:
    config = _config(tmp_path)
    dataset = load_dataset(ensure_normalized(config), config.data_config)
    candles = dataset.candles

    result = run_on_slice(config, candles, 0, 100, tmp_path, "train")

    assert isinstance(result, SegmentRun)
    assert result.label == "train"
    assert result.statistics.trade_count > 0
    assert (tmp_path / "XAUUSD_H1_train.csv").exists()
    loaded = load_dataset(tmp_path / "XAUUSD_H1_train.csv", config.data_config)
    assert len(loaded.candles) == 100


def test_run_on_slice_uses_frozen_config(tmp_path: Path) -> None:
    config = _config(tmp_path)
    dataset = load_dataset(ensure_normalized(config), config.data_config)
    candles = dataset.candles

    segment = run_on_slice(config, candles, 0, len(candles), tmp_path, "full")
    baseline = load_dataset(tmp_path / "XAUUSD_H1_full.csv", config.data_config)
    full = load_dataset(config.normalized_dataset, config.data_config)
    assert len(baseline.candles) == len(full.candles) == 400
    assert segment.statistics.trade_count > 0


def test_run_on_slice_rejects_invalid_bounds(tmp_path: Path) -> None:
    config = _config(tmp_path)
    dataset = load_dataset(ensure_normalized(config), config.data_config)
    candles = dataset.candles

    with pytest.raises(ValueError):
        run_on_slice(config, candles, 50, 50, tmp_path, "empty")
    with pytest.raises(ValueError):
        run_on_slice(config, candles, 100, 50, tmp_path, "reversed")
    with pytest.raises(ValueError):
        run_on_slice(config, candles, -1, 10, tmp_path, "negative")
    with pytest.raises(ValueError):
        run_on_slice(config, candles, 0, len(candles) + 1, tmp_path, "overflow")


def test_run_on_slice_is_deterministic(tmp_path: Path) -> None:
    config = _config(tmp_path)
    dataset = load_dataset(ensure_normalized(config), config.data_config)
    candles = dataset.candles

    first = run_on_slice(config, candles, 100, 300, tmp_path, "a")
    second = run_on_slice(config, candles, 100, 300, tmp_path, "b")
    assert first.statistics == second.statistics
    assert first.label != second.label
