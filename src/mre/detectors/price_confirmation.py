"""Price confirmation detector (ENG-002 §7.3)."""

from __future__ import annotations

from collections.abc import Sequence

from mre.models.candle import Candle
from mre.models.event import PRICE_CONFIRMATION, Event


def detect_price_confirmation(
    candles: Sequence[Candle],
    lookback: int = 20,
    source_detector: str = "price_confirmation",
) -> tuple[Event, ...]:
    """Detect price confirmation breakouts.

    A PRICE_CONFIRMATION occurs when a candle's close exceeds the
    highest high of the previous `lookback` candles (strictly greater).
    The current candle is excluded from its own window.

    Pure function: reads only price candles; independent of other
    detectors (Article 2).
    """
    if lookback < 1:
        raise ValueError("lookback must be >= 1")
    if not candles:
        raise ValueError("candles must not be empty")

    events: list[Event] = []
    for i in range(lookback, len(candles)):
        highest = max(c.high for c in candles[i - lookback : i])
        close = candles[i].close
        if close > highest:
            events.append(
                Event(
                    event_type=PRICE_CONFIRMATION,
                    timestamp=candles[i].timestamp,
                    source_detector=source_detector,
                    reference=i,
                    payload={"close": close, "highest_high": highest},
                    confirmable_at=candles[i].timestamp,
                    confirmable_ref=i,
                )
            )
    return tuple(events)
