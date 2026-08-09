from __future__ import annotations

import dataclasses

import pytest

from mre.models.execution import ExecutionConfig


def test_execution_config_defaults() -> None:
    config = ExecutionConfig()
    assert config.position_size == 1.0
    assert config.commission_rate == 0.0
    assert config.slippage_rate == 0.0
    assert config.hold_bars == 10
    assert config.stop_loss is None
    assert config.take_profit is None
    assert config.stop_loss_atr is None
    assert config.take_profit_atr is None
    assert config.atr_period == 14


def test_execution_config_holds_fields() -> None:
    config = ExecutionConfig(
        position_size=2.0,
        commission_rate=0.001,
        slippage_rate=0.0005,
        hold_bars=5,
        stop_loss=9.0,
        take_profit=12.0,
        stop_loss_atr=2.0,
        take_profit_atr=3.0,
        atr_period=20,
    )
    assert config.position_size == 2.0
    assert config.commission_rate == 0.001
    assert config.slippage_rate == 0.0005
    assert config.hold_bars == 5
    assert config.stop_loss == 9.0
    assert config.take_profit == 12.0
    assert config.stop_loss_atr == 2.0
    assert config.take_profit_atr == 3.0
    assert config.atr_period == 20


def test_execution_config_is_frozen() -> None:
    config = ExecutionConfig()
    with pytest.raises(dataclasses.FrozenInstanceError):
        config.hold_bars = 3


def test_execution_config_validation() -> None:
    with pytest.raises(ValueError):
        ExecutionConfig(position_size=0)
    with pytest.raises(ValueError):
        ExecutionConfig(position_size=-1.0)
    with pytest.raises(ValueError):
        ExecutionConfig(commission_rate=-0.01)
    with pytest.raises(ValueError):
        ExecutionConfig(slippage_rate=-0.01)
    with pytest.raises(ValueError):
        ExecutionConfig(hold_bars=0)
    with pytest.raises(ValueError):
        ExecutionConfig(hold_bars=-3)
    with pytest.raises(ValueError):
        ExecutionConfig(stop_loss=-5.0)
    with pytest.raises(ValueError):
        ExecutionConfig(take_profit=0)
    with pytest.raises(ValueError):
        ExecutionConfig(stop_loss_atr=0)
    with pytest.raises(ValueError):
        ExecutionConfig(stop_loss_atr=-2.0)
    with pytest.raises(ValueError):
        ExecutionConfig(take_profit_atr=-3.0)
    with pytest.raises(ValueError):
        ExecutionConfig(atr_period=0)
