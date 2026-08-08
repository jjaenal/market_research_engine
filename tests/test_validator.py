from __future__ import annotations

from datetime import datetime, timezone

import pytest

from mre.loaders.validator import ValidationError, validate
from mre.models.candle import Candle


def _candle(hour: int, open_: float = 10.0, high: float = 11.0, low: float = 9.0, close: float = 10.5, volume: float = 100.0) -> Candle:
    return Candle(
        timestamp=datetime(2020, 1, 1, hour, tzinfo=timezone.utc),
        open=open_,
        high=high,
        low=low,
        close=close,
        volume=volume,
    )


def test_validate_accepts_ordered_candles() -> None:
    candles = [_candle(0), _candle(1), _candle(2)]
    validate(candles)


def test_validate_rejects_duplicate_timestamp() -> None:
    candles = [_candle(0), _candle(0)]
    with pytest.raises(ValidationError, match="duplicate"):
        validate(candles)


def test_validate_rejects_unsorted_candles() -> None:
    candles = [_candle(2), _candle(0)]
    with pytest.raises(ValidationError, match="order|sorted|increasing"):
        validate(candles)


def test_validate_rejects_non_positive_price() -> None:
    candles = [_candle(0, open_=0.0)]
    with pytest.raises(ValidationError, match="open|price"):
        validate(candles)


def test_validate_rejects_high_below_max_open_close() -> None:
    candles = [_candle(0, open_=10.0, high=8.0, close=12.0)]
    with pytest.raises(ValidationError, match="high"):
        validate(candles)


def test_validate_rejects_low_above_min_open_close() -> None:
    candles = [_candle(0, open_=10.0, low=13.0, close=9.0)]
    with pytest.raises(ValidationError, match="low"):
        validate(candles)


def test_validate_rejects_negative_volume() -> None:
    candles = [_candle(0, volume=-1.0)]
    with pytest.raises(ValidationError, match="volume"):
        validate(candles)
