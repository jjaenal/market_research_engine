"""Raw trading-data export normalization (ARC-004 §7 CSV contract)."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

REQUIRED_COLUMNS = ("timestamp", "open", "high", "low", "close", "volume")


@dataclass(frozen=True)
class RawCsvConfig:
    """Format of a raw (header-less) OHLCV export."""

    timestamp_format: str = "%Y-%m-%d %H:%M"
    timezone: datetime.tzinfo = timezone.utc


def normalize_raw_csv(source: Path, target: Path, config: RawCsvConfig | None = None) -> Path:
    """Write a compliant dataset CSV (header + timezone-aware timestamps).

    Raw exports (e.g. ``datasets/XAUUSD_H1.csv``) are header-less with
    naive timestamps; this derives an immutable compliant snapshot per
    ARC-004 §7. The source file is never modified (Article 13).
    """
    cfg = config if config is not None else RawCsvConfig()

    with source.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.reader(handle)
        rows: list[list[str]] = []
        for i, row in enumerate(reader, start=1):
            if len(row) != 6:
                raise ValueError(f"row {i}: expected 6 columns, got {len(row)}")
            raw_ts, open_, high, low, close, volume = row
            timestamp = datetime.strptime(raw_ts.strip(), cfg.timestamp_format)
            timestamp = timestamp.replace(tzinfo=cfg.timezone)
            rows.append(
                [
                    timestamp.isoformat(),
                    open_.strip(),
                    high.strip(),
                    low.strip(),
                    close.strip(),
                    volume.strip(),
                ]
            )

    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(list(REQUIRED_COLUMNS))
        writer.writerows(rows)

    return target
