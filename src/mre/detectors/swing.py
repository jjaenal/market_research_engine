"""Fractal swing detector (ENG-002 §7.1, ADR-003)."""

from __future__ import annotations

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
    """Detect swing highs/lows using a fractal window (ADR-003).

    A swing_high at index i requires values[i] > every value in
    [i-left, i+right] (excluding i); swing_low is symmetric. Windows at
    the series edges that are not full produce no swings.

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
                )
            )
    return tuple(events)
