"""Sensitivity analysis tests (TODO-024, RSH-003 §9)."""

from __future__ import annotations

from pathlib import Path

import pytest

from mre.core.experiment_runner import ExperimentConfig, IndicatorConfig
from mre.core.sensitivity import (
    EXP001_GRID,
    SensitivityResult,
    SensitivityRun,
    _vary,
    run_sensitivity,
    to_markdown,
)
from mre.models.execution import ExecutionConfig
from mre.strategies import EXP001_STRATEGY_ID


def _config(tmp_path: Path) -> ExperimentConfig:
    return ExperimentConfig(
        experiment_id="EXP-001",
        title="t",
        hypothesis="h",
        code_version="test",
        generated_on="2026-08-08",
        strategy={"rsi_period": 14, "signal_window": 5, "hold_bars": 10},
        raw_dataset=Path("datasets/XAUUSD_H1.csv"),
        normalized_dataset=tmp_path / "XAUUSD_H1_normalized.csv",
        report_path=tmp_path / "report.md",
        indicator_config=IndicatorConfig(rsi_period=14),
        strategy_id=EXP001_STRATEGY_ID,
        execution_config=ExecutionConfig(hold_bars=10),
    )


def test_vary_rsi_period(tmp_path: Path) -> None:
    cfg = _vary(_config(tmp_path), "rsi_period", 21)
    assert cfg.indicator_config.rsi_period == 21
    assert cfg.execution_config.hold_bars == 10


def test_vary_swing_left(tmp_path: Path) -> None:
    cfg = _vary(_config(tmp_path), "swing_left", 3)
    assert cfg.event_config.swing_left == 3
    assert cfg.event_config.swing_right == 2


def test_vary_signal_window(tmp_path: Path) -> None:
    cfg = _vary(_config(tmp_path), "signal_window", 10)
    assert all(r.window == 10 for r in cfg.signal_definition)
    assert cfg.indicator_config.rsi_period == 14


def test_vary_hold_bars(tmp_path: Path) -> None:
    cfg = _vary(_config(tmp_path), "hold_bars", 20)
    assert cfg.execution_config.hold_bars == 20


def test_vary_unknown_parameter(tmp_path: Path) -> None:
    with pytest.raises(ValueError):
        _vary(_config(tmp_path), "unknown_param", 1.0)


def test_run_sensitivity_reuses_normalized_dataset(tmp_path: Path) -> None:
    normalized = tmp_path / "XAUUSD_H1_normalized.csv"
    result = run_sensitivity(_config(tmp_path), {"rsi_period": (7, 14, 21)}, dataset_path=normalized)
    assert normalized.exists()
    assert isinstance(result, SensitivityResult)
    assert result.baseline.trade_count > 0
    assert len(result.runs) == 3
    assert {r.value for r in result.for_parameter("rsi_period")} == {7, 14, 21}


def test_control_run_matches_baseline(tmp_path: Path) -> None:
    normalized = tmp_path / "XAUUSD_H1_normalized.csv"
    result = run_sensitivity(_config(tmp_path), {"rsi_period": (14, 21)}, dataset_path=normalized)
    control = next(r for r in result.runs if r.parameter == "rsi_period" and r.value == 14)
    assert control.statistics == result.baseline


def test_to_markdown_contains_all_runs(tmp_path: Path) -> None:
    normalized = tmp_path / "XAUUSD_H1_normalized.csv"
    result = run_sensitivity(_config(tmp_path), {"hold_bars": (5, 10)}, dataset_path=normalized)
    md = to_markdown(result, code_version="abc123", generated_on="2026-08-08",
                     strategy={"hold_bars": 10})
    assert "abc123" in md
    assert "Parameter: hold_bars" in md
    assert "| 5 |" in md
    assert "| 10 |" in md


def test_exp001_grid_contains_control_values() -> None:
    assert 14 in EXP001_GRID["rsi_period"]
    assert 20 in EXP001_GRID["price_lookback"]
    assert 5 in EXP001_GRID["signal_window"]
    assert 10 in EXP001_GRID["hold_bars"]
    assert 2 in EXP001_GRID["swing_left"]
    assert 2 in EXP001_GRID["swing_right"]
