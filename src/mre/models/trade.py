"""Trade domain model (ARC-002 §7.9)."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta

from mre.models.order import Order
from mre.models.position import Position


@dataclass(frozen=True)
class Trade:
    """One completed research transaction lifecycle (FND-009 §15.4)."""

    trade_id: str
    entry: Order
    position: Position
    exit: Order
    result: str
    holding_period: timedelta
    pnl: float
