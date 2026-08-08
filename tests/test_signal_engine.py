from __future__ import annotations

from datetime import datetime, timezone

import pytest

from mre.engines.signal_engine import combine
from mre.models.event import PRICE_CONFIRMATION, RSI_TRENDLINE_BROKEN, Event
from mre.models.signal_rule import SignalRule


def _ts(h: int) -> datetime:
    return datetime(2026, 1, 1, h, tzinfo=timezone.utc)


def _ev(event_type: str, ref: int) -> Event:
    return Event(
        event_type=event_type,
        timestamp=_ts(ref),
        source_detector="test",
        reference=ref,
        payload={"value": float(ref)},
    )


def _long_rule(window: int = 5) -> SignalRule:
    return SignalRule(
        signal_type="LONG",
        trigger=RSI_TRENDLINE_BROKEN,
        confirmations=(PRICE_CONFIRMATION,),
        window=window,
        source_strategy="rsi_trendline_breakout",
    )


def test_combine_returns_tuple_of_signals() -> None:
    events = [_ev(RSI_TRENDLINE_BROKEN, 10), _ev(PRICE_CONFIRMATION, 12)]
    signals = combine(events, [_long_rule()])
    assert isinstance(signals, tuple)
    assert len(signals) == 1


def test_combine_valid_signal_fields() -> None:
    events = [_ev(RSI_TRENDLINE_BROKEN, 10), _ev(PRICE_CONFIRMATION, 12)]
    (signal,) = combine(events, [_long_rule()])
    assert signal.signal_type == "LONG"
    assert signal.timestamp == _ts(12)
    assert signal.confirmation is True
    assert signal.source_strategy == "rsi_trendline_breakout"
    assert {e.event_type for e in signal.events} == {RSI_TRENDLINE_BROKEN, PRICE_CONFIRMATION}
    assert [e.reference for e in signal.events] == [10, 12]


def test_combine_window_boundary() -> None:
    within = combine([_ev(RSI_TRENDLINE_BROKEN, 10), _ev(PRICE_CONFIRMATION, 15)], [_long_rule(window=5)])
    assert len(within) == 1
    outside = combine([_ev(RSI_TRENDLINE_BROKEN, 10), _ev(PRICE_CONFIRMATION, 16)], [_long_rule(window=5)])
    assert outside == ()


def test_combine_picks_earliest_confirmation() -> None:
    events = [_ev(RSI_TRENDLINE_BROKEN, 10), _ev(PRICE_CONFIRMATION, 12), _ev(PRICE_CONFIRMATION, 13)]
    (signal,) = combine(events, [_long_rule()])
    assert signal.timestamp == _ts(12)


def test_combine_multiple_triggers() -> None:
    events = [
        _ev(RSI_TRENDLINE_BROKEN, 10),
        _ev(PRICE_CONFIRMATION, 12),
        _ev(RSI_TRENDLINE_BROKEN, 20),
        _ev(PRICE_CONFIRMATION, 22),
    ]
    signals = combine(events, [_long_rule()])
    assert [s.timestamp for s in signals] == [_ts(12), _ts(22)]


def test_combine_no_confirmation() -> None:
    assert combine([_ev(RSI_TRENDLINE_BROKEN, 10)], [_long_rule()]) == ()


def test_combine_empty_events() -> None:
    assert combine([], [_long_rule()]) == ()


def test_combine_empty_definition_raises() -> None:
    with pytest.raises(ValueError):
        combine([_ev(RSI_TRENDLINE_BROKEN, 10)], [])


def test_combine_rejects_non_int_reference() -> None:
    bad = Event(
        event_type=PRICE_CONFIRMATION,
        timestamp=_ts(12),
        source_detector="test",
        reference=None,
    )
    with pytest.raises(ValueError):
        combine([_ev(RSI_TRENDLINE_BROKEN, 10), bad], [_long_rule()])


def test_combine_unsorted_events_still_works() -> None:
    events = [_ev(PRICE_CONFIRMATION, 12), _ev(RSI_TRENDLINE_BROKEN, 10)]
    (signal,) = combine(events, [_long_rule()])
    assert signal.timestamp == _ts(12)


def test_combine_deterministic() -> None:
    events = [_ev(RSI_TRENDLINE_BROKEN, 10), _ev(PRICE_CONFIRMATION, 12)]
    assert combine(events, [_long_rule()]) == combine(events, [_long_rule()])


def test_combine_ignores_other_event_types() -> None:
    events = [
        _ev(RSI_TRENDLINE_BROKEN, 10),
        _ev("SWING_HIGH", 11),
        _ev(PRICE_CONFIRMATION, 12),
    ]
    (signal,) = combine(events, [_long_rule()])
    assert {e.event_type for e in signal.events} == {RSI_TRENDLINE_BROKEN, PRICE_CONFIRMATION}
