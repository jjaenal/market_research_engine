from __future__ import annotations

import dataclasses

import pytest

from mre.models.order import Order


def test_order_holds_fields() -> None:
    order = Order(
        order_type="market",
        side="long",
        price=10.5,
        trigger=3,
        execution_status="executed",
    )
    assert order.order_type == "market"
    assert order.side == "long"
    assert order.price == 10.5
    assert order.trigger == 3
    assert order.execution_status == "executed"


def test_order_is_frozen() -> None:
    order = Order(order_type="market", side="long", price=10.0, trigger=0, execution_status="executed")
    with pytest.raises(dataclasses.FrozenInstanceError):
        order.price = 99.0
