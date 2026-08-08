"""Exponential Moving Average (ENG-008 §7.1)."""

from __future__ import annotations

import math
from collections.abc import Sequence


def ema(closes: Sequence[float], period: int) -> list[float]:
    """Compute EMA seeded with SMA over the first `period` values.

    No lookahead: value at index i depends only on closes[0..i].
    Returns NaN for the first `period - 1` positions (warm-up).
    """
    if not closes:
        raise ValueError("closes must not be empty")
    if period < 1:
        raise ValueError("period must be >= 1")
    if len(closes) < period:
        return [math.nan] * len(closes)

    result: list[float] = [math.nan] * (period - 1)
    alpha = 2.0 / (period + 1)

    seed = sum(closes[:period]) / period
    result.append(seed)

    prev = seed
    for close in closes[period:]:
        prev = alpha * close + (1.0 - alpha) * prev
        result.append(prev)

    return result
