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


def test_rule_defaults_to_empty_payload_filter() -> None:
    rule = SignalRule(signal_type="LONG", trigger="A", confirmations=("B",), window=3)
    assert rule.trigger_payload == {}


def test_rule_accepts_payload_filter() -> None:
    rule = SignalRule(
        signal_type="LONG",
        trigger="RSI_TRENDLINE_BROKEN",
        confirmations=("PRICE_CONFIRMATION",),
        window=5,
        trigger_payload={"slope__lt": 0.0},
    )
    assert rule.trigger_payload == {"slope__lt": 0.0}


def test_rule_rejects_unknown_operator() -> None:
    with pytest.raises(ValueError):
        SignalRule(
            signal_type="LONG",
            trigger="A",
            confirmations=("B",),
            window=3,
            trigger_payload={"slope__between": 0.0},
        )


def test_rule_rejects_empty_filter_field() -> None:
    with pytest.raises(ValueError):
        SignalRule(
            signal_type="LONG",
            trigger="A",
            confirmations=("B",),
            window=3,
            trigger_payload={"__lt": 0.0},
        )


def test_rule_rejects_non_string_filter_key() -> None:
    with pytest.raises(ValueError):
        SignalRule(
            signal_type="LONG",
            trigger="A",
            confirmations=("B",),
            window=3,
            trigger_payload={1: 0.0},  # type: ignore[dict-item]
        )


def test_payload_matches_empty_filter() -> None:
    from mre.models.signal_rule import payload_matches

    assert payload_matches({"slope": 0.5}, {}) is True
    assert payload_matches(None, {}) is True


def test_payload_matches_exact_and_comparison() -> None:
    from mre.models.signal_rule import payload_matches

    assert payload_matches({"slope": -0.5, "value": 3.0}, {"slope__lt": 0.0}) is True
    assert payload_matches({"slope": 0.5}, {"slope__lt": 0.0}) is False
    assert payload_matches({"slope": 0.5}, {"slope__ge": 0.5}) is True
    assert payload_matches({"slope": 0.5}, {"slope": 0.5}) is True
    assert payload_matches({"slope": 0.5}, {"slope": 0.6}) is False
    assert payload_matches({"slope": 0.5}, {"slope": 0.6, "value__gt": 1.0}) is False
    assert payload_matches({"value": 2.0}, {"slope__lt": 0.0}) is False
    assert payload_matches(None, {"slope__lt": 0.0}) is False
    assert payload_matches({"slope": 0.5}, {"slope__neq": 0.6}) is True
