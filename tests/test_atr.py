from __future__ import annotations

import math

import pytest

from mre.indicators.atr import atr
from mre.models.candle import Candle

from datetime import datetime, timezone


def _candle(high: float, low: float, close: float, idx: int) -> Candle:
    return Candle(
        timestamp=datetime(2020, 1, 1, idx, tzinfo=timezone.utc),
        open=close,
        high=high,
        low=low,
        close=close,
        volume=100.0,
    )


def test_atr_warmup_is_nan() -> None:
    candles = [_candle(10, 9, 9.5, i) for i in range(20)]
    result = atr(candles, period=14)
    assert len(result) == len(candles)
    assert all(math.isnan(v) for v in result[:14])


def test_atr_reference_values() -> None:
    highs = [10.0, 10.5, 10.8, 11.0, 11.2, 11.5, 11.4, 11.6, 11.8, 12.0, 12.2, 12.4, 12.6, 12.8, 13.0, 13.2]
    lows = [9.5, 9.8, 10.0, 10.2, 10.4, 10.6, 10.8, 11.0, 11.2, 11.4, 11.6, 11.8, 12.0, 12.2, 12.4, 12.6]
    closes = [9.7, 10.0, 10.3, 10.6, 10.9, 11.2, 11.5, 11.8, 12.1, 12.4, 12.7, 13.0, 13.3, 13.6, 13.9, 14.2]
    candles = [_candle(highs[i], lows[i], closes[i], i) for i in range(len(highs))]

    tr = [highs[0] - lows[0]]
    for i in range(1, len(candles)):
        tr.append(
            max(
                highs[i] - lows[i],
                abs(highs[i] - closes[i - 1]),
                abs(lows[i] - closes[i - 1]),
            )
        )

    result = atr(candles, period=14)
    expected = [math.nan] * 14
    prev = sum(tr[1:15]) / 14
    expected.append(prev)
    for i in range(15, len(candles)):
        prev = (prev * 13 + tr[i]) / 14
        expected.append(prev)

    for got, want in zip(result, expected):
        if math.isnan(want):
            assert math.isnan(got)
        else:
            assert math.isclose(got, want, rel_tol=1e-9)


def test_atr_is_deterministic() -> None:
    candles = [_candle(10 + i * 0.5, 9 + i * 0.5, 9.5 + i * 0.5, i) for i in range(20)]
    assert atr(candles, period=14) == atr(candles, period=14)


def test_atr_no_lookahead() -> None:
    candles = [_candle(10 + i * 0.5, 9 + i * 0.5, 9.5 + i * 0.5, i) for i in range(20)]
    result = atr(candles, period=14)
    truncated = atr(candles[:17], period=14)
    for i in range(17):
        if math.isnan(result[i]):
            assert math.isnan(truncated[i])
        else:
            assert math.isclose(result[i], truncated[i], rel_tol=1e-9)


def test_atr_rejects_empty() -> None:
    with pytest.raises(ValueError):
        atr([], period=14)
