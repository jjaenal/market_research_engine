from __future__ import annotations

from datetime import datetime, timezone

import pytest

from mre.detectors.swing import detect_swings
from mre.models.event import SWING_HIGH, SWING_LOW


def _ts(i: int) -> datetime:
    return datetime(2026, 1, 1, i, tzinfo=timezone.utc)


def _timestamps(n: int) -> list[datetime]:
    return [_ts(i) for i in range(n)]


VALUES = [1.0, 2.0, 3.0, 2.0, 1.0, 2.0, 3.0, 4.0, 3.0, 2.0, 1.0, 2.0, 3.0, 4.0, 5.0]


def test_swing_high_low_positions() -> None:
    events = detect_swings(VALUES, _timestamps(len(VALUES)), left=2, right=2)
    highs = [e.reference for e in events if e.event_type == SWING_HIGH]
    lows = [e.reference for e in events if e.event_type == SWING_LOW]
    assert highs == [2, 7]
    assert lows == [4, 10]


def test_swing_event_metadata() -> None:
    events = detect_swings(VALUES, _timestamps(len(VALUES)), left=2, right=2)
    high = next(e for e in events if e.event_type == SWING_HIGH and e.reference == 2)
    assert high.source_detector == "swing"
    assert high.timestamp == _ts(2)
    assert high.payload == {"value": 3.0}


def test_swing_carries_confirmable_timing() -> None:
    events = detect_swings(VALUES, _timestamps(len(VALUES)), left=2, right=2)
    high = next(e for e in events if e.event_type == SWING_HIGH and e.reference == 2)
    assert high.confirmable_ref == 4
    assert high.confirmable_at == _ts(4)
    low = next(e for e in events if e.event_type == SWING_LOW and e.reference == 4)
    assert low.confirmable_ref == 6
    assert low.confirmable_at == _ts(6)


def test_no_swing_at_partial_edge_windows() -> None:
    events = detect_swings(VALUES, _timestamps(len(VALUES)), left=2, right=2)
    assert all(e.reference not in (0, 1, 13, 14) for e in events)


def test_flat_series_produces_no_swings() -> None:
    flat = [1.0] * 10
    assert detect_swings(flat, _timestamps(len(flat)), left=2, right=2) == ()


def test_nan_warmup_region_produces_no_swings() -> None:
    import math

    nan_series = [math.nan] * 14 + [10, 12, 11, 13, 12, 14]
    assert detect_swings(nan_series, _timestamps(len(nan_series)), left=2, right=2) == ()


def test_nan_neighbor_disqualifies_candidate() -> None:
    import math

    values = [3.0, math.nan, 3.0, 2.0, 4.0, 1.0, 3.0, 2.0, 5.0, 2.0, 3.0, 4.0, 2.0, 1.0, 3.0]
    events = detect_swings(values, _timestamps(len(values)), left=2, right=2)
    assert all(e.reference != 2 for e in events)


def test_configurable_window() -> None:
    events = detect_swings(VALUES, _timestamps(len(VALUES)), left=1, right=1)
    highs = [e.reference for e in events if e.event_type == SWING_HIGH]
    lows = [e.reference for e in events if e.event_type == SWING_LOW]
    assert highs == [2, 7]
    assert lows == [4, 10]


def test_deterministic() -> None:
    assert detect_swings(VALUES, _timestamps(len(VALUES)), left=2, right=2) == detect_swings(
        VALUES, _timestamps(len(VALUES)), left=2, right=2
    )


def test_rejects_invalid_window() -> None:
    ts = _timestamps(len(VALUES))
    with pytest.raises(ValueError):
        detect_swings(VALUES, ts, left=0, right=2)
    with pytest.raises(ValueError):
        detect_swings(VALUES, ts, left=2, right=-1)


def test_rejects_empty_or_mismatched() -> None:
    with pytest.raises(ValueError):
        detect_swings([], _timestamps(0), left=2, right=2)
    with pytest.raises(ValueError):
        detect_swings(VALUES, _timestamps(len(VALUES) - 1), left=2, right=2)
