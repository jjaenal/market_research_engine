from __future__ import annotations

import dataclasses
from datetime import datetime, timezone

import pytest

from mre.models.event import (
    Event,
    PRICE_CONFIRMATION,
    RSI_TRENDLINE_BROKEN,
    RSI_TRENDLINE_CREATED,
    SWING_HIGH,
    SWING_LOW,
)


def _ts(i: int = 0) -> datetime:
    return datetime(2026, 1, 1, i, tzinfo=timezone.utc)


def test_event_holds_fields() -> None:
    ts = _ts()
    event = Event(
        event_type=SWING_HIGH,
        timestamp=ts,
        source_detector="swing",
        reference=5,
        payload={"value": 42.0},
        experiment_id="EXP-0001",
    )
    assert event.event_type == SWING_HIGH
    assert event.timestamp == ts
    assert event.source_detector == "swing"
    assert event.reference == 5
    assert event.payload == {"value": 42.0}
    assert event.experiment_id == "EXP-0001"


def test_event_defaults() -> None:
    event = Event(event_type=SWING_LOW, timestamp=_ts(), source_detector="swing")
    assert event.reference is None
    assert event.payload is None
    assert event.experiment_id == ""


def test_event_is_frozen() -> None:
    event = Event(event_type=SWING_LOW, timestamp=_ts(), source_detector="swing")
    with pytest.raises(dataclasses.FrozenInstanceError):
        event.event_type = RSI_TRENDLINE_CREATED


def test_event_type_constants() -> None:
    assert SWING_HIGH == "SWING_HIGH"
    assert SWING_LOW == "SWING_LOW"
    assert RSI_TRENDLINE_CREATED == "RSI_TRENDLINE_CREATED"
    assert RSI_TRENDLINE_BROKEN == "RSI_TRENDLINE_BROKEN"
    assert PRICE_CONFIRMATION == "PRICE_CONFIRMATION"
