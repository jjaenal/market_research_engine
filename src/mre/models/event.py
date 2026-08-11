"""Event domain model (ARC-003 §7)."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

SWING_HIGH = "SWING_HIGH"
SWING_LOW = "SWING_LOW"
RSI_TRENDLINE_CREATED = "RSI_TRENDLINE_CREATED"
RSI_TRENDLINE_BROKEN = "RSI_TRENDLINE_BROKEN"
PRICE_CONFIRMATION = "PRICE_CONFIRMATION"


@dataclass(frozen=True)
class Event:
    """A detected atomic fact emitted by a detector.

    Immutable per FND-001 Article 13; deterministic per Article 7;
    a fact, not a recommendation, per Article 3.

    ``timestamp`` is the time at which the fact is established (for a
    swing, the peak bar). ``confirmable_at``/``confirmable_ref`` carry
    the earliest time/bar at which the fact is *knowable* — for a fractal
    swing that is the confirmation bar ``peak + right`` (SPEC-001, ADR-005).
    Events that are knowable at their own timestamp leave these as None.
    """

    event_type: str
    timestamp: datetime
    source_detector: str
    reference: Any = None
    payload: Any = field(default=None)
    experiment_id: str = ""
    confirmable_at: datetime | None = None
    confirmable_ref: int | None = None
