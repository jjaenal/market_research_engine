"""Dataset and dataset metadata models (ARC-002 §7.2, ARC-004 §6.2)."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from mre.models.candle import Candle


@dataclass(frozen=True)
class DatasetMetadata:
    """Immutable dataset metadata (ARC-004 §6.2)."""

    dataset_version: str
    symbol: str
    timeframe: str
    timezone: str
    source: str
    date_range: tuple[datetime, datetime]
    candle_count: int
    integrity_status: str


@dataclass(frozen=True)
class Dataset:
    """Validated, immutable dataset (Article 13)."""

    metadata: DatasetMetadata
    candles: tuple[Candle, ...]


@dataclass(frozen=True)
class DataConfig:
    """Dataset configuration (FR-012, config over hardcode)."""

    symbol: str
    timeframe: str
    timezone: str = "UTC"
    source: str = "csv"
