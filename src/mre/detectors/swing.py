"""Fractal swing detector (ENG-002 §7.1, ADR-003)."""

from __future__ import annotations

import math
from collections.abc import Sequence
from datetime import datetime

from mre.models.event import SWING_HIGH, SWING_LOW, Event


def detect_swings(
    values: Sequence[float],
    timestamps: Sequence[datetime],
    left: int = 2,
    right: int = 2,
    source_detector: str = "swing",
) -> tuple[Event, ...]:
    """Detect swing highs/lows using a fractal window (ADR-003, SPEC-001).

    A swing_high at index i requires values[i] > every value in
    [i-left, i+right] (excluding i); swing_low is symmetric. Windows at
    the series edges that are not full produce no swings. Any NaN in
    the window disqualifies the candidate (SPEC-001 §4.5): an unknown
    value cannot certify an extremum, so warm-up regions emit no events.

    No lookahead (SPEC-001, ADR-005): the event timestamp is the peak
    bar ``i`` (the fact), but the swing is only *knowable* after the
    right confirmation window closes, so ``confirmable_at`` is the
    timestamp of bar ``i + right`` and ``confirmable_ref`` is ``i + right``.
    Consumers must not act on the event before its confirmable time.

    Pure function: reads only `values` and `timestamps` (Article 2).
    """
    if left < 1 or right < 1:
        raise ValueError("left and right must be >= 1")
    if not values:
        raise ValueError("values must not be empty")
    if len(values) != len(timestamps):
        raise ValueError("values and timestamps must have equal length")
    if len(values) <= left + right:
        return ()

    events: list[Event] = []
    n = len(values)
    for i in range(left, n - right):
        window = values[i - left : i + right + 1]
        if any(math.isnan(v) for v in window):
            continue
        high = True
        low = True
        for j in range(i - left, i + right + 1):
            if j == i:
                continue
            if values[i] <= values[j]:
                high = False
            if values[i] >= values[j]:
                low = False
        if high:
            events.append(
                Event(
                    event_type=SWING_HIGH,
                    timestamp=timestamps[i],
                    source_detector=source_detector,
                    reference=i,
                    payload={"value": values[i]},
                    confirmable_at=timestamps[i + right],
                    confirmable_ref=i + right,
                )
            )
        if low:
            events.append(
                Event(
                    event_type=SWING_LOW,
                    timestamp=timestamps[i],
                    source_detector=source_detector,
                    reference=i,
                    payload={"value": values[i]},
                    confirmable_at=timestamps[i + right],
                    confirmable_ref=i + right,
                )
            )
    return tuple(events)
