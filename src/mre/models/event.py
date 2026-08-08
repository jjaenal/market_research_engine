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
    """

    event_type: str
    timestamp: datetime
    source_detector: str
    reference: Any = None
    payload: Any = field(default=None)
    experiment_id: str = ""
