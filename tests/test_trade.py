from __future__ import annotations

import dataclasses
from datetime import datetime, timedelta, timezone

import pytest

from mre.models.order import Order
from mre.models.position import Position
from mre.models.trade import Trade


def _ts(h: int) -> datetime:
    return datetime(2026, 1, 1, h, tzinfo=timezone.utc)


def _order(price: float, trigger: int) -> Order:
    return Order(order_type="market", side="long", price=price, trigger=trigger, execution_status="executed")


def _position() -> Position:
    return Position(side="long", entry_price=10.0, size=1.0, opened_at=_ts(1), closed_at=_ts(4))


def test_trade_holds_fields() -> None:
    trade = Trade(
        trade_id="T-0001",
        entry=_order(10.0, 1),
        position=_position(),
        exit=_order(13.0, 4),
        result="WIN",
        holding_period=timedelta(hours=3),
        pnl=3.0,
    )
    assert trade.trade_id == "T-0001"
    assert trade.entry.price == 10.0
    assert trade.position.side == "long"
    assert trade.exit.price == 13.0
    assert trade.result == "WIN"
    assert trade.holding_period == timedelta(hours=3)
    assert trade.pnl == 3.0


def test_trade_is_frozen() -> None:
    trade = Trade(
        trade_id="T-0001",
        entry=_order(10.0, 1),
        position=_position(),
        exit=_order(13.0, 4),
        result="WIN",
        holding_period=timedelta(hours=3),
        pnl=3.0,
    )
    with pytest.raises(dataclasses.FrozenInstanceError):
        trade.pnl = 0.0
