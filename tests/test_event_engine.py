from __future__ import annotations

from datetime import datetime, timezone

import pytest

from mre.engines.event_engine import EventEngine, EventEngineConfig
from mre.models.candle import Candle
from mre.models.dataset import Dataset, DatasetMetadata
from mre.models.event import (
    PRICE_CONFIRMATION,
    RSI_TRENDLINE_BROKEN,
    RSI_TRENDLINE_CREATED,
    SWING_HIGH,
    SWING_LOW,
    Event,
)


def _ts(i: int) -> datetime:
    return datetime(2026, 1, 1, i, tzinfo=timezone.utc)


def _candles(closes: list[float]) -> tuple[Candle, ...]:
    candles: list[Candle] = []
    for i, c in enumerate(closes):
        prev = closes[i - 1] if i > 0 else c
        candles.append(Candle(timestamp=_ts(i), open=prev, high=c + 2.0, low=c - 2.0, close=c, volume=0.0))
    return tuple(candles)


def _dataset(closes: list[float]) -> Dataset:
    candles = _candles(closes)
    metadata = DatasetMetadata(
        dataset_version="1.0.0",
        symbol="TEST",
        timeframe="H1",
        timezone="UTC",
        source="fixture",
        date_range=(candles[0].timestamp, candles[-1].timestamp),
        candle_count=len(candles),
        integrity_status="valid",
    )
    return Dataset(metadata=metadata, candles=candles)


def _engine() -> EventEngine:
    return EventEngine(config=EventEngineConfig(swing_left=2, swing_right=2, price_lookback=5))


PRICE = [30.0, 33.0, 35.0, 32.0, 28.0, 30.0, 34.0, 37.0, 40.0, 38.0, 41.0, 44.0, 46.0, 43.0, 40.0, 36.0, 32.0, 34.0, 37.0, 39.0, 36.0, 33.0, 29.0, 31.0]
RSI = [30.0, 33.0, 35.0, 32.0, 28.0, 30.0, 34.0, 37.0, 40.0, 38.0, 41.0, 44.0, 46.0, 43.0, 40.0, 36.0, 32.0, 34.0, 37.0, 39.0, 36.0, 33.0, 29.0, 31.0]


def test_engine_emits_sorted_timeline() -> None:
    events = _engine().detect(_dataset(PRICE), {"rsi": RSI})
    assert isinstance(events, tuple)
    assert all(isinstance(e, Event) for e in events)
    assert events == tuple(sorted(events, key=lambda e: (e.timestamp, e.source_detector, e.event_type)))


def test_engine_contains_all_event_types() -> None:
    events = _engine().detect(_dataset(PRICE), {"rsi": RSI})
    types = {e.event_type for e in events}
    assert SWING_HIGH in types
    assert SWING_LOW in types
    assert RSI_TRENDLINE_CREATED in types
    assert RSI_TRENDLINE_BROKEN in types
    assert PRICE_CONFIRMATION in types


def test_engine_trendline_break_after_created() -> None:
    events = _engine().detect(_dataset(PRICE), {"rsi": RSI})
    created = [e.timestamp for e in events if e.event_type == RSI_TRENDLINE_CREATED]
    broken = [e.timestamp for e in events if e.event_type == RSI_TRENDLINE_BROKEN]
    assert broken and created and all(b > c for b in broken for c in created)


def test_engine_requires_rsi_series() -> None:
    with pytest.raises(ValueError):
        _engine().detect(_dataset(PRICE), {})


def test_engine_deterministic() -> None:
    a = _engine().detect(_dataset(PRICE), {"rsi": RSI})
    b = _engine().detect(_dataset(PRICE), {"rsi": RSI})
    assert a == b


def test_engine_config_knobs() -> None:
    events = _engine().detect(_dataset(PRICE), {"rsi": RSI})
    assert len(events) > 0
