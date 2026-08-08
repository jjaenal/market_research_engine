"""Position domain model (ARC-002 §7.8)."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Position:
    """Active exposure to an instrument (FND-009 §15.1)."""

    side: str
    entry_price: float
    size: float
    opened_at: datetime
    closed_at: datetime | None
