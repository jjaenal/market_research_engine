from __future__ import annotations

import dataclasses

import pytest

from mre.models.signal_rule import SignalRule


def test_signal_rule_holds_fields() -> None:
    rule = SignalRule(
        signal_type="LONG",
        trigger="RSI_TRENDLINE_BROKEN",
        confirmations=("PRICE_CONFIRMATION",),
        window=5,
        source_strategy="rsi_trendline_breakout",
    )
    assert rule.signal_type == "LONG"
    assert rule.trigger == "RSI_TRENDLINE_BROKEN"
    assert rule.confirmations == ("PRICE_CONFIRMATION",)
    assert rule.window == 5
    assert rule.source_strategy == "rsi_trendline_breakout"


def test_signal_rule_default_source() -> None:
    rule = SignalRule(signal_type="SHORT", trigger="A", confirmations=("B",), window=3)
    assert rule.source_strategy == ""


def test_signal_rule_is_frozen() -> None:
    rule = SignalRule(signal_type="LONG", trigger="A", confirmations=("B",), window=3)
    with pytest.raises(dataclasses.FrozenInstanceError):
        rule.window = 10


def test_rule_rejects_empty_signal_type() -> None:
    with pytest.raises(ValueError):
        SignalRule(signal_type="", trigger="A", confirmations=("B",), window=3)


def test_rule_rejects_empty_trigger() -> None:
    with pytest.raises(ValueError):
        SignalRule(signal_type="LONG", trigger="", confirmations=("B",), window=3)


def test_rule_rejects_empty_confirmations() -> None:
    with pytest.raises(ValueError):
        SignalRule(signal_type="LONG", trigger="A", confirmations=(), window=3)


def test_rule_rejects_duplicate_confirmations() -> None:
    with pytest.raises(ValueError):
        SignalRule(signal_type="LONG", trigger="A", confirmations=("B", "B"), window=3)


def test_rule_rejects_invalid_window() -> None:
    with pytest.raises(ValueError):
        SignalRule(signal_type="LONG", trigger="A", confirmations=("B",), window=0)
    with pytest.raises(ValueError):
        SignalRule(signal_type="LONG", trigger="A", confirmations=("B",), window=-2)
