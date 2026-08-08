"""Relative Strength Index (Wilder) — ENG-008 §7.2."""

from __future__ import annotations

import math
from collections.abc import Sequence


def rsi(closes: Sequence[float], period: int = 14) -> list[float]:
    """Compute Wilder RSI.

    No lookahead: value at index i depends only on closes[0..i].
    Returns NaN for the first `period` positions (warm-up).
    """
    if period < 1:
        raise ValueError("period must be >= 1")
    if not closes:
        raise ValueError("closes must not be empty")
    if len(closes) <= period:
        return [math.nan] * len(closes)

    result: list[float] = [math.nan] * period

    deltas = [closes[i] - closes[i - 1] for i in range(1, len(closes))]

    avg_gain = sum(max(d, 0.0) for d in deltas[:period]) / period
    avg_loss = sum(max(-d, 0.0) for d in deltas[:period]) / period

    for i in range(period, len(closes)):
        gain = max(deltas[i - 1], 0.0)
        loss = max(-deltas[i - 1], 0.0)
        avg_gain = (avg_gain * (period - 1) + gain) / period
        avg_loss = (avg_loss * (period - 1) + loss) / period

        if avg_loss == 0:
            result.append(100.0)
        else:
            rs = avg_gain / avg_loss
            result.append(100.0 - 100.0 / (1.0 + rs))

    return result
