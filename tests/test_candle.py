from __future__ import annotations

from datetime import datetime, timezone

import dataclasses

import pytest

from mre.models.candle import Candle


def test_candle_holds_ohlcv_fields() -> None:
    ts = datetime(2020, 1, 1, tzinfo=timezone.utc)
    candle = Candle(timestamp=ts, open=1520.10, high=1522.00, low=1518.50, close=1521.30, volume=1000.0)

    assert candle.timestamp == ts
    assert candle.open == 1520.10
    assert candle.high == 1522.00
    assert candle.low == 1518.50
    assert candle.close == 1521.30
    assert candle.volume == 1000.0


def test_candle_is_frozen() -> None:
    ts = datetime(2020, 1, 1, tzinfo=timezone.utc)
    candle = Candle(timestamp=ts, open=1.0, high=2.0, low=0.5, close=1.5, volume=10.0)

    with pytest.raises(dataclasses.FrozenInstanceError):
        candle.close = 9.9
