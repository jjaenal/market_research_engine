"""Candle domain model (ARC-002 §7.3, ARC-004 §6.1)."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Candle:
    """One market observation within a timeframe.

    Immutable per FND-001 Article 13. Timezone-aware timestamp required.
    """

    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float
