from __future__ import annotations

import csv
from datetime import timezone

import pytest

from mre.loaders.normalize import RawCsvConfig, normalize_raw_csv
from mre.models.candle import Candle


def _write_raw(path, rows: list[str]) -> None:
    path.write_text("\n".join(rows) + "\n", encoding="utf-8")


def test_normalize_adds_header_and_tz_timestamps(tmp_path) -> None:
    raw = tmp_path / "raw.csv"
    out = tmp_path / "out.csv"
    _write_raw(
        raw,
        [
            "2020-01-01 00:00,100.0,101.0,99.0,100.5,10",
            "2020-01-01 01:00,100.5,101.5,99.5,101.0,12",
        ],
    )

    normalize_raw_csv(raw, out)

    with out.open(encoding="utf-8") as handle:
        rows = list(csv.reader(handle))
    assert rows[0] == ["timestamp", "open", "high", "low", "close", "volume"]
    assert len(rows) == 3
    ts = rows[1][0]
    assert ts.endswith("+00:00")
    assert ts.startswith("2020-01-01T00:00:00")
    assert rows[2][1:] == ["100.5", "101.5", "99.5", "101.0", "12"]


def test_normalize_writes_compliant_loadable_dataset(tmp_path) -> None:
    raw = tmp_path / "raw.csv"
    out = tmp_path / "out.csv"
    _write_raw(
        raw,
        [
            "2020-01-01 00:00,1.0,1.5,0.5,1.2,3",
            "2020-01-01 01:00,1.2,1.8,1.0,1.6,4",
        ],
    )

    normalize_raw_csv(raw, out)

    from mre.loaders.csv_loader import load_dataset
    from mre.models.dataset import DataConfig

    dataset = load_dataset(out, DataConfig(symbol="XAUUSD", timeframe="H1"))
    assert dataset.metadata.candle_count == 2
    first: Candle = dataset.candles[0]
    assert first.timestamp.tzinfo == timezone.utc
    assert first.close == 1.2


def test_normalize_rejects_wrong_column_count(tmp_path) -> None:
    raw = tmp_path / "raw.csv"
    out = tmp_path / "out.csv"
    _write_raw(raw, ["2020-01-01 00:00,100.0,101.0,99.0,100.5"])

    with pytest.raises(ValueError):
        normalize_raw_csv(raw, out)


def test_normalize_rejects_malformed_timestamp(tmp_path) -> None:
    raw = tmp_path / "raw.csv"
    out = tmp_path / "out.csv"
    _write_raw(raw, ["not-a-date,100.0,101.0,99.0,100.5,10"])

    with pytest.raises(ValueError):
        normalize_raw_csv(raw, out)


def test_normalize_custom_format_and_tz(tmp_path) -> None:
    raw = tmp_path / "raw.csv"
    out = tmp_path / "out.csv"
    _write_raw(raw, ["01/02/2020,10.0,11.0,9.0,10.5,1"])

    normalize_raw_csv(raw, out, RawCsvConfig(timestamp_format="%d/%m/%Y", timezone=timezone.utc))

    with out.open(encoding="utf-8") as handle:
        rows = list(csv.reader(handle))
    assert rows[1][0] == "2020-02-01T00:00:00+00:00"
