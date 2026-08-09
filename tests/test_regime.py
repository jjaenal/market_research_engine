from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest

from mre.indicators.regime import HIGH, LOW, volatility_regime
from mre.models.candle import Candle


def _candle(idx: int, high: float, low: float) -> Candle:
    return Candle(
        timestamp=datetime(2020, 1, 1, tzinfo=timezone.utc) + timedelta(minutes=idx),
        open=(high + low) / 2,
        high=high,
        low=low,
        close=(high + low) / 2,
        volume=100.0,
    )


def test_regime_warmup_is_none() -> None:
    candles = [_candle(i, 10, 9) for i in range(120)]
    labels = volatility_regime(candles, short_period=14, long_period=100)
    assert len(labels) == len(candles)
    assert all(label is None for label in labels[:100])
    assert all(label in (HIGH, LOW) for label in labels[100:])


def test_regime_expanding_volatility_is_high() -> None:
    candles = [_candle(i, 10 + i * 0.1, 9) for i in range(200)]
    labels = volatility_regime(candles, short_period=14, long_period=100)
    assert all(label == HIGH for label in labels[120:])


def test_regime_contracting_volatility_is_low() -> None:
    candles = [
        _candle(i, 20, 19) if i < 150 else _candle(i, 20, 19.9)
        for i in range(300)
    ]
    labels = volatility_regime(candles, short_period=14, long_period=100)
    assert all(label == LOW for label in labels[250:])


def test_regime_is_deterministic() -> None:
    candles = [_candle(i, 10 + (i % 7), 9) for i in range(150)]
    assert volatility_regime(candles) == volatility_regime(candles)


def test_regime_no_lookahead() -> None:
    candles = [_candle(i, 10 + (i % 11), 9) for i in range(150)]
    full = volatility_regime(candles, 14, 100)
    truncated = volatility_regime(candles[:130], 14, 100)
    for i in range(130):
        assert full[i] == truncated[i]


def test_regime_rejects_empty() -> None:
    with pytest.raises(ValueError):
        volatility_regime([])


def test_regime_rejects_bad_periods() -> None:
    candles = [_candle(i, 10, 9) for i in range(10)]
    with pytest.raises(ValueError):
        volatility_regime(candles, short_period=0)
    with pytest.raises(ValueError):
        volatility_regime(candles, long_period=0)
    with pytest.raises(ValueError):
        volatility_regime(candles, short_period=50, long_period=14)
