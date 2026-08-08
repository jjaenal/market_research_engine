from __future__ import annotations

import dataclasses
from datetime import datetime, timezone

import pytest

from mre.models.event import PRICE_CONFIRMATION, RSI_TRENDLINE_BROKEN, Event
from mre.models.signal import Signal


def _ts(h: int = 0) -> datetime:
    return datetime(2026, 1, 1, h, tzinfo=timezone.utc)


def _ev(event_type: str, ref: int) -> Event:
    return Event(
        event_type=event_type,
        timestamp=_ts(ref),
        source_detector="test",
        reference=ref,
        payload={"value": float(ref)},
    )


def test_signal_holds_fields() -> None:
    ts = _ts(7)
    events = (_ev(RSI_TRENDLINE_BROKEN, 5), _ev(PRICE_CONFIRMATION, 7))
    signal = Signal(
        signal_type="LONG",
        timestamp=ts,
        events=events,
        confirmation=True,
        source_strategy="rsi_trendline_breakout",
        experiment_id="EXP-0001",
    )
    assert signal.signal_type == "LONG"
    assert signal.timestamp == ts
    assert signal.events == events
    assert signal.confirmation is True
    assert signal.source_strategy == "rsi_trendline_breakout"
    assert signal.experiment_id == "EXP-0001"


def test_signal_defaults() -> None:
    signal = Signal(signal_type="LONG", timestamp=_ts(), events=())
    assert signal.confirmation is True
    assert signal.source_strategy == ""
    assert signal.experiment_id == ""


def test_signal_is_frozen() -> None:
    signal = Signal(signal_type="LONG", timestamp=_ts(), events=())
    with pytest.raises(dataclasses.FrozenInstanceError):
        signal.signal_type = "SHORT"


def test_signal_events_tuple_of_events() -> None:
    ev = _ev(PRICE_CONFIRMATION, 3)
    signal = Signal(signal_type="LONG", timestamp=ev.timestamp, events=(ev,))
    assert signal.events == (ev,)
