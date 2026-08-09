"""Market volatility regime classification (ARC-008 §14, FND-006 §17 RQ).

Regime selection labels each candle as ``"high"`` or ``"low"`` volatility
by comparing short ATR to its own longer-horizon ATR: when the short-horizon
ATR is >= the long-horizon ATR the market is in an expanding/high-volatility
regime, otherwise in a contracting/low-volatility regime. Warm-up candles
(before the long ATR is defined) are labeled ``None``.
"""

from __future__ import annotations

import math
from collections.abc import Sequence

from mre.indicators.atr import atr
from mre.models.candle import Candle

HIGH = "high"
LOW = "low"


def volatility_regime(
    candles: Sequence[Candle],
    short_period: int = 14,
    long_period: int = 100,
) -> list[str | None]:
    """Label each candle ``"high"``/``"low"`` volatility or ``None`` (warm-up).

    No lookahead: the label at index ``i`` depends only on candles[0..i].
    The regime is the direction of short-horizon volatility relative to its
    longer-horizon baseline (expanding vs contracting), pre-registered per
    experiment (Article 12) and deterministic (Article 7).
    """
    if not candles:
        raise ValueError("candles must not be empty")
    if short_period < 1 or long_period < 1:
        raise ValueError("short_period and long_period must be >= 1")
    if long_period < short_period:
        raise ValueError("long_period must be >= short_period")

    short = atr(candles, short_period)
    long_ = atr(candles, long_period)

    labels: list[str | None] = []
    for short_value, long_value in zip(short, long_):
        if math.isnan(short_value) or math.isnan(long_value) or long_value == 0.0:
            labels.append(None)
        elif short_value >= long_value:
            labels.append(HIGH)
        else:
            labels.append(LOW)
    return labels
