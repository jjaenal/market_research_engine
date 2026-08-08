"""RSI trendline detector (ENG-002 §7.2, ADR-004)."""

from __future__ import annotations

from collections.abc import Sequence
from datetime import datetime

from mre.detectors.swing import detect_swings
from mre.models.event import RSI_TRENDLINE_BROKEN, RSI_TRENDLINE_CREATED, Event

_SOURCE = "rsi_trendline"


def detect_rsi_trendline(
    values: Sequence[float],
    timestamps: Sequence[datetime],
    left: int = 2,
    right: int = 2,
    source_detector: str = _SOURCE,
) -> tuple[Event, ...]:
    """Detect RSI trendline create/break events (ADR-004).

    Up-trendlines connect the last two swing lows (slope > 0);
    down-trendlines connect the last two swing highs (slope < 0).
    A line is created when the newer swing is confirmed, and broken the
    first time the RSI crosses below (up) or above (down) the line.

    Pure function: reads only the RSI `values` (Article 2).
    """
    if not values:
        raise ValueError("values must not be empty")
    if len(values) != len(timestamps):
        raise ValueError("values and timestamps must have equal length")

    swings = detect_swings(values, timestamps, left=left, right=right, source_detector=source_detector)

    lows = [
        (e.reference, e.payload["value"])
        for e in swings
        if e.event_type == "SWING_LOW"
    ]
    highs = [
        (e.reference, e.payload["value"])
        for e in swings
        if e.event_type == "SWING_HIGH"
    ]

    events: list[Event] = []
    events.extend(_build(values, timestamps, lows, broken_below=True, source_detector=source_detector))
    events.extend(_build(values, timestamps, highs, broken_below=False, source_detector=source_detector))
    return tuple(sorted(events, key=lambda e: (e.timestamp, e.event_type, e.reference)))


def _build(
    values: Sequence[float],
    timestamps: Sequence[datetime],
    points: list[tuple[int, float]],
    broken_below: bool,
    source_detector: str,
) -> list[Event]:
    events: list[Event] = []
    for k in range(1, len(points)):
        a_index, a_value = points[k - 1]
        b_index, b_value = points[k]
        slope = (b_value - a_value) / (b_index - a_index)

        if broken_below and slope <= 0:
            continue
        if not broken_below and slope >= 0:
            continue

        events.append(
            Event(
                event_type=RSI_TRENDLINE_CREATED,
                timestamp=timestamps[b_index],
                source_detector=source_detector,
                reference=b_index,
                payload={
                    "value": b_value,
                    "slope": slope,
                    "start": a_index,
                    "end": b_index,
                },
            )
        )

        for t in range(b_index + 1, len(values)):
            line_value = a_value + slope * (t - a_index)
            if (broken_below and values[t] < line_value) or (not broken_below and values[t] > line_value):
                events.append(
                    Event(
                        event_type=RSI_TRENDLINE_BROKEN,
                        timestamp=timestamps[t],
                        source_detector=source_detector,
                        reference=t,
                        payload={
                            "value": values[t],
                            "line_value": line_value,
                            "slope": slope,
                            "start": a_index,
                            "end": b_index,
                        },
                    )
                )
                break
    return events
