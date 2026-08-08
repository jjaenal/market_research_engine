from __future__ import annotations

from datetime import datetime, timezone

import pytest

from mre.detectors.price_confirmation import detect_price_confirmation
from mre.models.candle import Candle
from mre.models.event import PRICE_CONFIRMATION


def _ts(i: int) -> datetime:
    return datetime(2026, 1, 1, i, tzinfo=timezone.utc)


def _candles(closes: list[float], spread: float = 0.5) -> list[Candle]:
    candles: list[Candle] = []
    for i, c in enumerate(closes):
        prev = closes[i - 1] if i > 0 else c
        candles.append(
            Candle(
                timestamp=_ts(i),
                open=prev,
                high=c + spread,
                low=c - spread,
                close=c,
                volume=0.0,
            )
        )
    return candles


CLOSES = [1.0, 2.0, 3.0, 2.0, 1.0, 2.0, 3.0, 4.0, 3.0, 2.0, 1.0, 2.0, 3.0, 4.0, 5.0]


def test_confirmation_positions() -> None:
    events = detect_price_confirmation(_candles(CLOSES), lookback=5)
    assert [e.reference for e in events] == [7, 13, 14]


def test_confirmation_metadata() -> None:
    events = detect_price_confirmation(_candles(CLOSES), lookback=5)
    event = next(e for e in events if e.reference == 7)
    assert event.event_type == PRICE_CONFIRMATION
    assert event.source_detector == "price_confirmation"
    assert event.timestamp == _ts(7)
    assert event.payload["close"] == 4.0
    assert event.payload["highest_high"] == 3.5


def test_warmup_has_no_confirmation() -> None:
    events = detect_price_confirmation(_candles(CLOSES), lookback=5)
    assert all(e.reference >= 5 for e in events)


def test_strict_breakout() -> None:
    flat = _candles([1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0])
    assert detect_price_confirmation(flat, lookback=5) == ()


def test_deterministic() -> None:
    assert detect_price_confirmation(_candles(CLOSES), lookback=5) == detect_price_confirmation(
        _candles(CLOSES), lookback=5
    )


def test_rejects_invalid_lookback() -> None:
    with pytest.raises(ValueError):
        detect_price_confirmation(_candles(CLOSES), lookback=0)
    with pytest.raises(ValueError):
        detect_price_confirmation(_candles(CLOSES), lookback=-1)
