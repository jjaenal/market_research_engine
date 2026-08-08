"""Average True Range (Wilder) — ENG-008 §7.3."""

from __future__ import annotations

import math
from collections.abc import Sequence

from mre.models.candle import Candle


def _true_range(candles: Sequence[Candle], index: int) -> float:
    candle = candles[index]
    if index == 0:
        return candle.high - candle.low
    prev_close = candles[index - 1].close
    return max(
        candle.high - candle.low,
        abs(candle.high - prev_close),
        abs(candle.low - prev_close),
    )


def atr(candles: Sequence[Candle], period: int = 14) -> list[float]:
    """Compute Wilder ATR.

    No lookahead: value at index i depends only on candles[0..i].
    Returns NaN for the first `period` positions (warm-up).
    """
    if period < 1:
        raise ValueError("period must be >= 1")
    if not candles:
        raise ValueError("candles must not be empty")
    if len(candles) <= period:
        return [math.nan] * len(candles)

    result: list[float] = [math.nan] * period

    true_ranges = [_true_range(candles, i) for i in range(len(candles))]

    prev = sum(true_ranges[1 : period + 1]) / period
    result.append(prev)

    for i in range(period + 1, len(candles)):
        prev = (prev * (period - 1) + true_ranges[i]) / period
        result.append(prev)

    return result
