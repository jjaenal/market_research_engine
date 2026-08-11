from __future__ import annotations

from datetime import datetime, timezone

import pytest

from mre.detectors.rsi_trendline import detect_rsi_trendline
from mre.models.event import RSI_TRENDLINE_BROKEN, RSI_TRENDLINE_CREATED


def _ts(i: int) -> datetime:
    return datetime(2026, 1, 1, i, tzinfo=timezone.utc)


def _timestamps(n: int) -> list[datetime]:
    return [_ts(i) for i in range(n)]


RSI_VALUES = [30, 33, 35, 32, 28, 30, 34, 37, 40, 38, 41, 44, 46, 43, 40, 36, 32, 34, 37, 39, 36, 33, 29, 31]


def test_trendline_created_and_broken() -> None:
    events = detect_rsi_trendline(RSI_VALUES, _timestamps(len(RSI_VALUES)), left=2, right=2)
    created = [(e.reference, e.payload.get("slope")) for e in events if e.event_type == RSI_TRENDLINE_CREATED]
    broken = [e.reference for e in events if e.event_type == RSI_TRENDLINE_BROKEN]

    assert created == [(16, pytest.approx(1 / 3)), (19, -1.0)]
    assert broken == [21]


def test_break_event_metadata() -> None:
    events = detect_rsi_trendline(RSI_VALUES, _timestamps(len(RSI_VALUES)), left=2, right=2)
    broken = next(e for e in events if e.event_type == RSI_TRENDLINE_BROKEN)
    assert broken.source_detector == "rsi_trendline"
    assert broken.timestamp == _ts(21)
    assert broken.payload["value"] == 33.0
    assert broken.payload["line_value"] > broken.payload["value"]


def test_events_carry_confirmable_timing() -> None:
    events = detect_rsi_trendline(RSI_VALUES, _timestamps(len(RSI_VALUES)), left=2, right=2)
    created = {e.reference: e for e in events if e.event_type == RSI_TRENDLINE_CREATED}
    assert created[16].confirmable_ref == 18
    assert created[16].confirmable_at == _ts(18)
    assert created[19].confirmable_ref == 21
    assert created[19].confirmable_at == _ts(21)
    broken = next(e for e in events if e.event_type == RSI_TRENDLINE_BROKEN)
    assert broken.confirmable_ref == 21
    assert broken.confirmable_at == _ts(21)


def test_no_trendline_without_two_swings() -> None:
    short = RSI_VALUES[:10]
    assert detect_rsi_trendline(short, _timestamps(len(short)), left=2, right=2) == ()


def test_flat_slope_does_not_create_up_trendline() -> None:
    values = [30.0, 32.0, 34.0, 31.0, 28.0, 30.0, 32.0, 34.0, 31.0, 28.0, 30.0, 32.0]
    events = detect_rsi_trendline(values, _timestamps(len(values)), left=2, right=2)
    created = [e for e in events if e.event_type == RSI_TRENDLINE_CREATED]
    assert all(not (e.payload.get("slope", 0.0) >= 0.0) for e in created)


def test_deterministic() -> None:
    assert detect_rsi_trendline(RSI_VALUES, _timestamps(len(RSI_VALUES)), left=2, right=2) == detect_rsi_trendline(
        RSI_VALUES, _timestamps(len(RSI_VALUES)), left=2, right=2
    )


def test_no_lookahead() -> None:
    full = detect_rsi_trendline(RSI_VALUES, _timestamps(len(RSI_VALUES)), left=2, right=2)
    prefix = detect_rsi_trendline(RSI_VALUES[:20], _timestamps(20), left=2, right=2)
    for e in prefix:
        assert e in full


def test_rejects_mismatched_lengths() -> None:
    with pytest.raises(ValueError):
        detect_rsi_trendline(RSI_VALUES, _timestamps(len(RSI_VALUES) - 1), left=2, right=2)
