"""Strategy plugin registry tests (ARC-008 ARC-ACT-010, ARC-005 §6/§10)."""

from __future__ import annotations

import pytest

from mre.core.experiment_runner import ExperimentConfig, exp001_config
from mre.models.event import PRICE_CONFIRMATION, RSI_TRENDLINE_BROKEN, SWING_HIGH
from mre.models.signal_rule import SignalRule
from mre.strategies import (
    EXP001_STRATEGY_ID,
    PRICE_BREAKOUT_STRATEGY_ID,
    SWING_BREAKOUT_STRATEGY_ID,
    get,
    register,
    registered_ids,
)
from mre.strategies.registry import _STRATEGIES


def test_exp001_strategy_registered() -> None:
    assert EXP001_STRATEGY_ID in registered_ids()
    definition = get(EXP001_STRATEGY_ID)
    assert len(definition) == 1
    rule = definition[0]
    assert rule.signal_type == "LONG"
    assert rule.trigger == RSI_TRENDLINE_BROKEN
    assert rule.confirmations == (PRICE_CONFIRMATION,)
    assert rule.source_strategy == EXP001_STRATEGY_ID


def test_exp005_price_breakout_registered() -> None:
    assert PRICE_BREAKOUT_STRATEGY_ID in registered_ids()
    definition = get(PRICE_BREAKOUT_STRATEGY_ID)
    assert len(definition) == 1
    rule = definition[0]
    assert rule.signal_type == "LONG"
    assert rule.trigger == PRICE_CONFIRMATION
    assert rule.confirmations == (SWING_HIGH,)
    assert rule.source_strategy == PRICE_BREAKOUT_STRATEGY_ID


def test_exp007_swing_breakout_registered() -> None:
    assert SWING_BREAKOUT_STRATEGY_ID in registered_ids()
    definition = get(SWING_BREAKOUT_STRATEGY_ID)
    assert len(definition) == 1
    rule = definition[0]
    assert rule.signal_type == "LONG"
    assert rule.trigger == SWING_HIGH
    assert rule.confirmations == (PRICE_CONFIRMATION,)
    assert rule.source_strategy == SWING_BREAKOUT_STRATEGY_ID


def test_get_unknown_strategy_raises() -> None:
    with pytest.raises(ValueError):
        get("not_a_real_strategy")


def test_register_requires_id() -> None:
    with pytest.raises(ValueError):
        register("", (SignalRule("LONG", "X", ("Y",), window=1),))


def test_register_requires_definition() -> None:
    with pytest.raises(ValueError):
        register("empty_def", ())


def test_register_rejects_duplicate() -> None:
    with pytest.raises(ValueError):
        register(EXP001_STRATEGY_ID, (SignalRule("LONG", "X", ("Y",), window=1),))


def test_registered_ids_deterministic() -> None:
    assert registered_ids() == tuple(sorted(_STRATEGIES))


def test_config_resolves_signal_definition_from_registry(tmp_path) -> None:
    cfg = exp001_config(tmp_path / "report.md")
    assert cfg.strategy_id == EXP001_STRATEGY_ID
    assert len(cfg.signal_definition) == 1
    assert cfg.signal_definition == get(EXP001_STRATEGY_ID)


def test_config_with_unknown_strategy_id_fails() -> None:
    with pytest.raises(ValueError):
        ExperimentConfig(
            experiment_id="X",
            title="t",
            hypothesis="h",
            code_version="test",
            generated_on="2026-08-08",
            strategy_id="does_not_exist",
        )
