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


def _ev_slope(event_type: str, ref: int, slope: float) -> Event:
    return Event(
        event_type=event_type,
        timestamp=_ts(ref),
        source_detector="test",
        reference=ref,
        payload={"value": float(ref), "slope": slope},
    )


def _ev_confirmable(event_type: str, ref: int, confirmable_ref: int) -> Event:
    return Event(
        event_type=event_type,
        timestamp=_ts(ref),
        source_detector="test",
        reference=ref,
        payload={"value": float(ref)},
        confirmable_at=_ts(confirmable_ref),
        confirmable_ref=confirmable_ref,
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


def test_combine_timestamp_is_latest_knowable_time() -> None:
    trigger = _ev_confirmable(RSI_TRENDLINE_BROKEN, 10, confirmable_ref=10)
    confirm = _ev_confirmable(PRICE_CONFIRMATION, 12, confirmable_ref=14)
    (signal,) = combine([trigger, confirm], [_long_rule()])
    assert signal.timestamp == _ts(14)


def test_combine_knowable_time_without_confirmable_fallback() -> None:
    trigger = _ev(RSI_TRENDLINE_BROKEN, 10)
    confirm = _ev(PRICE_CONFIRMATION, 12)
    (signal,) = combine([trigger, confirm], [_long_rule()])
    assert signal.timestamp == _ts(12)


def test_combine_knowable_time_mixed_fallback() -> None:
    trigger = _ev_confirmable(RSI_TRENDLINE_BROKEN, 10, confirmable_ref=13)
    confirm = _ev(PRICE_CONFIRMATION, 12)
    (signal,) = combine([trigger, confirm], [_long_rule()])
    assert signal.timestamp == _ts(13)


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


def test_combine_filters_triggers_by_payload() -> None:
    rule = SignalRule(
        signal_type="LONG",
        trigger=RSI_TRENDLINE_BROKEN,
        confirmations=(PRICE_CONFIRMATION,),
        window=5,
        trigger_payload={"slope__lt": 0.0},
    )
    bullish = _ev_slope(RSI_TRENDLINE_BROKEN, 10, slope=-1.0)
    bearish = _ev_slope(RSI_TRENDLINE_BROKEN, 20, slope=1.0)
    confirm = _ev(PRICE_CONFIRMATION, 12)
    events = [bullish, bearish, confirm]

    signals = combine(events, [rule])

    assert len(signals) == 1
    (signal,) = signals
    assert signal.signal_type == "LONG"
    assert signal.timestamp == _ts(12)
    assert bullish in signal.events
    assert bearish not in signal.events


def test_combine_trigger_filter_excludes_without_confirm() -> None:
    rule = SignalRule(
        signal_type="LONG",
        trigger=RSI_TRENDLINE_BROKEN,
        confirmations=(PRICE_CONFIRMATION,),
        window=5,
        trigger_payload={"slope__gt": 0.0},
    )
    bullish = _ev_slope(RSI_TRENDLINE_BROKEN, 10, slope=-1.0)
    confirm = _ev(PRICE_CONFIRMATION, 12)
    assert combine([bullish, confirm], [rule]) == ()


def _long_rule_with_cooldown(cooldown: int, window: int = 5) -> SignalRule:
    return SignalRule(
        signal_type="LONG",
        trigger=RSI_TRENDLINE_BROKEN,
        confirmations=(PRICE_CONFIRMATION,),
        window=window,
        source_strategy="rsi_trendline_breakout",
        cooldown=cooldown,
    )


def test_combine_cooldown_collapses_overlapping_triggers() -> None:
    events = [
        _ev(RSI_TRENDLINE_BROKEN, 10),
        _ev(RSI_TRENDLINE_BROKEN, 11),
        _ev(RSI_TRENDLINE_BROKEN, 12),
        _ev(PRICE_CONFIRMATION, 13),
    ]
    signals = combine(events, [_long_rule_with_cooldown(cooldown=1)])
    assert len(signals) == 1
    assert signals[0].timestamp == _ts(13)


def test_combine_cooldown_zero_keeps_legacy_behavior() -> None:
    events = [
        _ev(RSI_TRENDLINE_BROKEN, 10),
        _ev(RSI_TRENDLINE_BROKEN, 11),
        _ev(RSI_TRENDLINE_BROKEN, 12),
        _ev(PRICE_CONFIRMATION, 13),
    ]
    signals = combine(events, [_long_rule_with_cooldown(cooldown=0)])
    assert len(signals) == 3
    assert [s.timestamp for s in signals] == [_ts(13), _ts(13), _ts(13)]


def test_combine_cooldown_allows_signals_at_exact_spacing() -> None:
    events = [
        _ev(RSI_TRENDLINE_BROKEN, 10),
        _ev(PRICE_CONFIRMATION, 12),
        _ev(RSI_TRENDLINE_BROKEN, 15),
        _ev(PRICE_CONFIRMATION, 17),
    ]
    signals = combine(events, [_long_rule_with_cooldown(cooldown=5)])
    assert len(signals) == 2
    assert [s.timestamp for s in signals] == [_ts(12), _ts(17)]


def test_combine_cooldown_suppresses_inside_gap() -> None:
    events = [
        _ev(RSI_TRENDLINE_BROKEN, 10),
        _ev(PRICE_CONFIRMATION, 12),
        _ev(RSI_TRENDLINE_BROKEN, 15),
        _ev(PRICE_CONFIRMATION, 17),
    ]
    signals = combine(events, [_long_rule_with_cooldown(cooldown=6)])
    assert len(signals) == 1
    assert signals[0].timestamp == _ts(12)


def test_combine_cooldown_tracks_last_emitted_reference() -> None:
    events = [
        _ev(RSI_TRENDLINE_BROKEN, 10),
        _ev(PRICE_CONFIRMATION, 12),
        _ev(RSI_TRENDLINE_BROKEN, 12),
        _ev(PRICE_CONFIRMATION, 14),
        _ev(RSI_TRENDLINE_BROKEN, 18),
        _ev(PRICE_CONFIRMATION, 20),
    ]
    signals = combine(events, [_long_rule_with_cooldown(cooldown=3)])
    assert [s.timestamp for s in signals] == [_ts(12), _ts(20)]


def test_combine_cooldown_uses_knowable_ref() -> None:
    events = [
        _ev_confirmable(RSI_TRENDLINE_BROKEN, 10, confirmable_ref=13),
        _ev_confirmable(PRICE_CONFIRMATION, 12, confirmable_ref=12),
        _ev_confirmable(RSI_TRENDLINE_BROKEN, 14, confirmable_ref=17),
        _ev_confirmable(PRICE_CONFIRMATION, 16, confirmable_ref=16),
    ]
    signals = combine(events, [_long_rule_with_cooldown(cooldown=5)])
    assert len(signals) == 1
    assert signals[0].timestamp == _ts(13)


def test_combine_cooldown_is_per_rule() -> None:
    rule_a = _long_rule_with_cooldown(cooldown=1)
    rule_b = SignalRule(
        signal_type="SHORT",
        trigger="SWING_LOW",
        confirmations=(PRICE_CONFIRMATION,),
        window=5,
        cooldown=1,
    )
    events = [
        _ev(RSI_TRENDLINE_BROKEN, 10),
        _ev(RSI_TRENDLINE_BROKEN, 11),
        _ev("SWING_LOW", 12),
        _ev(PRICE_CONFIRMATION, 13),
    ]
    signals = combine(events, [rule_a, rule_b])
    assert [s.signal_type for s in signals] == ["LONG", "SHORT"]
