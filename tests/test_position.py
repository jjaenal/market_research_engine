from __future__ import annotations

import dataclasses
from datetime import datetime, timezone

import pytest

from mre.models.position import Position


def _ts(h: int) -> datetime:
    return datetime(2026, 1, 1, h, tzinfo=timezone.utc)


def test_position_holds_fields() -> None:
    position = Position(
        side="long",
        entry_price=10.0,
        size=1.5,
        opened_at=_ts(1),
        closed_at=_ts(4),
    )
    assert position.side == "long"
    assert position.entry_price == 10.0
    assert position.size == 1.5
    assert position.opened_at == _ts(1)
    assert position.closed_at == _ts(4)


def test_position_is_frozen() -> None:
    position = Position(side="long", entry_price=10.0, size=1.0, opened_at=_ts(1), closed_at=None)
    with pytest.raises(dataclasses.FrozenInstanceError):
        position.size = 2.0
