"""External experiment config (YAML) loader tests (ARC-008 ARC-ACT-011, FR-012)."""

from __future__ import annotations

from pathlib import Path

import pytest

from mre.core.experiment_runner import (
    DEFAULT_EXPERIMENT_CONFIG,
    exp001_config,
    load_experiment_config,
)
from mre.strategies import EXP001_STRATEGY_ID, get as get_strategy


EXPECTED_SECTIONS = """\
experiment:
  id: EXP-001
  title: T
  hypothesis: H
  strategy_id: {strategy_id}

dataset:
  symbol: XAUUSD
  timeframe: H1
  timezone: UTC
  source: csv

indicator:
  rsi_period: 21

event:
  swing_left: 1
  swing_right: 3
  price_lookback: 12

execution:
  position_size: 2.0
  commission_rate: 0.001
  slippage_rate: 0.0005
  hold_bars: 8
  stop_loss: null
  take_profit: null
  stop_loss_atr: null
  take_profit_atr: null
  atr_period: 14

statistics:
  min_sample: 50

regime:
  atr_short_period: 7
  atr_long_period: 60
  selected_regime: high

signal:
  cooldown: 5

paths:
  raw_dataset: datasets/XAUUSD_H1.csv
  normalized_dataset: experiments/EXP-001/dataset/XAUUSD_H1_normalized.csv
  report_path: experiments/EXP-001/EXP-001_report.md
"""


def _write(path: Path, content: str) -> Path:
    path.write_text(content, encoding="utf-8")
    return path


def test_default_config_file_is_committed() -> None:
    assert DEFAULT_EXPERIMENT_CONFIG.exists(), "configs/EXP-001.yaml must be committed (FR-010)"
    cfg = load_experiment_config(DEFAULT_EXPERIMENT_CONFIG)
    assert cfg.experiment_id == "EXP-001"
    assert cfg.strategy_id == EXP001_STRATEGY_ID


def test_load_experiment_config_maps_all_sections(tmp_path: Path) -> None:
    path = _write(tmp_path / "cfg.yaml", EXPECTED_SECTIONS.format(strategy_id=EXP001_STRATEGY_ID))
    cfg = load_experiment_config(path)

    assert cfg.experiment_id == "EXP-001"
    assert cfg.title == "T"
    assert cfg.hypothesis == "H"
    assert cfg.strategy_id == EXP001_STRATEGY_ID
    assert cfg.signal_definition != get_strategy(EXP001_STRATEGY_ID)
    assert len(cfg.signal_definition) == len(get_strategy(EXP001_STRATEGY_ID))
    for rule, base in zip(cfg.signal_definition, get_strategy(EXP001_STRATEGY_ID)):
        assert rule.cooldown == 5
        assert rule.signal_type == base.signal_type
        assert rule.trigger == base.trigger

    assert cfg.data_config.symbol == "XAUUSD"
    assert cfg.data_config.timeframe == "H1"
    assert cfg.data_config.timezone == "UTC"
    assert cfg.data_config.source == "csv"

    assert cfg.indicator_config.rsi_period == 21
    assert cfg.event_config.swing_left == 1
    assert cfg.event_config.swing_right == 3
    assert cfg.event_config.price_lookback == 12

    assert cfg.execution_config.position_size == 2.0
    assert cfg.execution_config.commission_rate == 0.001
    assert cfg.execution_config.slippage_rate == 0.0005
    assert cfg.execution_config.hold_bars == 8
    assert cfg.execution_config.stop_loss is None
    assert cfg.execution_config.take_profit is None
    assert cfg.execution_config.stop_loss_atr is None
    assert cfg.execution_config.take_profit_atr is None
    assert cfg.execution_config.atr_period == 14

    assert cfg.statistics_config.min_sample == 50
    assert cfg.regime_config.atr_short_period == 7
    assert cfg.regime_config.atr_long_period == 60
    assert cfg.regime_config.selected_regime == "high"
    assert cfg.signal_cooldown == 5
    assert all(rule.cooldown == 5 for rule in cfg.signal_definition)
    assert cfg.raw_dataset == Path("datasets/XAUUSD_H1.csv")
    assert cfg.normalized_dataset == Path("experiments/EXP-001/dataset/XAUUSD_H1_normalized.csv")
    assert cfg.report_path == Path("experiments/EXP-001/EXP-001_report.md")


def test_load_experiment_config_derives_strategy_summary(tmp_path: Path) -> None:
    path = _write(tmp_path / "cfg.yaml", EXPECTED_SECTIONS.format(strategy_id=EXP001_STRATEGY_ID))
    cfg = load_experiment_config(path)

    assert cfg.strategy["rsi_period"] == 21
    assert cfg.strategy["swing_left"] == 1
    assert cfg.strategy["swing_right"] == 3
    assert cfg.strategy["price_lookback"] == 12
    assert cfg.strategy["signal_window"] == 5
    assert cfg.strategy["signal_cooldown"] == 5
    assert cfg.strategy["regime"] == "high"
    assert cfg.strategy["regime_atr_short"] == 7
    assert cfg.strategy["regime_atr_long"] == 60
    assert cfg.strategy["hold_bars"] == 8
    assert cfg.strategy["trigger_payload"] == "RSI_TRENDLINE_BROKEN slope__lt 0.0"


def test_load_experiment_config_missing_file_raises(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="config file not found"):
        load_experiment_config(tmp_path / "nope.yaml")


def test_load_experiment_config_invalid_yaml_raises(tmp_path: Path) -> None:
    path = _write(tmp_path / "bad.yaml", "experiment: [unclosed\n  nope")
    with pytest.raises(ValueError, match="invalid YAML"):
        load_experiment_config(path)


def test_load_experiment_config_missing_section_raises(tmp_path: Path) -> None:
    path = _write(tmp_path / "missing.yaml", "experiment:\n  id: X\n")
    with pytest.raises(ValueError, match="missing or invalid 'dataset' section"):
        load_experiment_config(path)


def test_load_experiment_config_unknown_strategy_raises(tmp_path: Path) -> None:
    content = EXPECTED_SECTIONS.format(strategy_id="does_not_exist")
    path = _write(tmp_path / "cfg.yaml", content)
    with pytest.raises(ValueError, match="unknown strategy plugin"):
        load_experiment_config(path)


def test_exp001_config_overrides_paths_only(tmp_path: Path) -> None:
    cfg = exp001_config(tmp_path / "out.md", source=tmp_path / "raw.csv")
    assert cfg.report_path == tmp_path / "out.md"
    assert cfg.raw_dataset == tmp_path / "raw.csv"
    assert cfg.experiment_id == "EXP-001"
    assert cfg.strategy_id == EXP001_STRATEGY_ID
