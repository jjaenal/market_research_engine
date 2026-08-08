"""Event Engine orchestration (ENG-002 §9, ARC-006 §7.3)."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass

from mre.detectors.price_confirmation import detect_price_confirmation
from mre.detectors.rsi_trendline import detect_rsi_trendline
from mre.detectors.swing import detect_swings
from mre.models.dataset import Dataset
from mre.models.event import Event

_RSI_KEY = "rsi"


@dataclass(frozen=True)
class EventEngineConfig:
    """Event Engine configuration (config over hardcode, FR-012)."""

    swing_left: int = 2
    swing_right: int = 2
    price_lookback: int = 20


class EventEngine:
    """Runs the configured detectors and merges the Event timeline.

    Each detector is independent (Article 2); the engine only collects
    and sorts their events by timestamp (Article 1).
    """

    def __init__(self, config: EventEngineConfig | None = None) -> None:
        self.config = config if config is not None else EventEngineConfig()

    def detect(self, dataset: Dataset, indicators: Mapping[str, Sequence[float]]) -> tuple[Event, ...]:
        """Produce the sorted Event timeline for a dataset.

        Requires the ``rsi`` indicator series aligned with the candles.
        """
        candles = dataset.candles
        timestamps = [c.timestamp for c in candles]

        if _RSI_KEY not in indicators:
            raise ValueError("rsi indicator series is required")

        closes = [c.close for c in candles]
        rsi_values = list(indicators[_RSI_KEY])
        if len(rsi_values) != len(candles):
            raise ValueError("rsi series must align with dataset candles")

        events: list[Event] = []
        events.extend(
            detect_swings(
                closes,
                timestamps,
                left=self.config.swing_left,
                right=self.config.swing_right,
            )
        )
        events.extend(
            detect_rsi_trendline(
                rsi_values,
                timestamps,
                left=self.config.swing_left,
                right=self.config.swing_right,
            )
        )
        events.extend(detect_price_confirmation(candles, lookback=self.config.price_lookback))

        return tuple(sorted(events, key=lambda e: (e.timestamp, e.source_detector, e.event_type)))
