"""CSV data loader (ARC-004 §7 CSV contract, FEAT-001)."""

from __future__ import annotations

import csv
import hashlib
from datetime import datetime
from pathlib import Path

from mre.loaders.validator import ValidationError, validate
from mre.models.candle import Candle
from mre.models.dataset import DataConfig, Dataset, DatasetMetadata

REQUIRED_COLUMNS = ("timestamp", "open", "high", "low", "close", "volume")


def load_dataset(source: Path, config: DataConfig) -> Dataset:
    """Load a CSV file into a validated, immutable Dataset (ARC-006 §7.1).

    Raises:
        FileNotFoundError: when the source file does not exist.
        ValidationError: when the CSV violates the ARC-004 contract or integrity rules.
    """
    if not source.exists():
        raise FileNotFoundError(f"dataset file not found: {source}")

    candles = _parse(source)

    validate(candles)

    first = candles[0].timestamp
    last = candles[-1].timestamp
    metadata = DatasetMetadata(
        dataset_version=_build_version(config, first, last, candles),
        symbol=config.symbol,
        timeframe=config.timeframe,
        timezone=config.timezone,
        source=config.source,
        date_range=(first, last),
        candle_count=len(candles),
        integrity_status="valid",
    )
    return Dataset(metadata=metadata, candles=tuple(candles))


def _parse(source: Path) -> list[Candle]:
    with source.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        columns = reader.fieldnames or []
        missing = [col for col in REQUIRED_COLUMNS if col not in columns]
        if missing:
            raise ValidationError(f"missing required columns: {', '.join(missing)}")

        candles: list[Candle] = []
        for row in reader:
            candles.append(_row_to_candle(row))

    return candles


def _row_to_candle(row: dict[str, str]) -> Candle:
    timestamp = _parse_timestamp(row.get("timestamp", ""))
    open_ = _to_float(row.get("open", ""), "open")
    high = _to_float(row.get("high", ""), "high")
    low = _to_float(row.get("low", ""), "low")
    close = _to_float(row.get("close", ""), "close")
    volume = _to_float(row.get("volume", ""), "volume")
    return Candle(
        timestamp=timestamp,
        open=open_,
        high=high,
        low=low,
        close=close,
        volume=volume,
    )


def _parse_timestamp(raw: str) -> datetime:
    if not raw.strip():
        raise ValidationError("empty timestamp value")
    try:
        parsed = datetime.fromisoformat(raw.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValidationError(f"malformed timestamp: {raw!r}") from exc
    if parsed.tzinfo is None:
        raise ValidationError(f"timestamp must be timezone-aware: {raw!r}")
    return parsed


def _to_float(raw: str, column: str) -> float:
    if not raw.strip():
        raise ValidationError(f"missing value for column: {column}")
    try:
        return float(raw)
    except ValueError as exc:
        raise ValidationError(f"column {column} is not a number: {raw!r}") from exc


def _build_version(
    config: DataConfig, first: datetime, last: datetime, candles: list[Candle]
) -> str:
    """Generate dataset_version per ARC-004 §10 + E-6 (content-addressed).

    Format: ``SYMBOL_TIMEFRAME_START_END_vNNN_<content8>`` where the
    trailing digest is derived from the candle content, so any change to
    the data (not just symbol/timeframe/range) yields a new version —
    the pre-E-6 version was content-blind and silently reused ``_v001``
    across different files. Pure function.
    """
    digest = _content_digest(candles)
    return f"{config.symbol}_{config.timeframe}_{first.year}_{last.year}_v001_{digest}"


def _content_digest(candles: list[Candle]) -> str:
    """First 8 hex chars of a SHA-256 over the candle content (E-6)."""
    hasher = hashlib.sha256()
    for candle in candles:
        hasher.update(f"{candle.timestamp.isoformat()}|{candle.open}|{candle.high}|{candle.low}|{candle.close}|{candle.volume}\n".encode("utf-8"))
    return hasher.hexdigest()[:8]
