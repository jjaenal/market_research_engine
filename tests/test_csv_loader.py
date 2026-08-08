from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import pytest

from mre.loaders.csv_loader import load_dataset
from mre.loaders.validator import ValidationError
from mre.models.dataset import DataConfig


def _write_csv(tmp_path: Path, content: str, name: str = "XAUUSD_H1.csv") -> Path:
    path = tmp_path / name
    path.write_text(content, encoding="utf-8")
    return path


VALID_CSV = """\
timestamp,open,high,low,close,volume
2020-01-01T00:00:00Z,1520.10,1522.00,1518.50,1521.30,1000
2020-01-01T01:00:00Z,1521.30,1523.10,1519.00,1522.40,1100
2020-01-01T02:00:00Z,1522.40,1524.50,1520.00,1523.00,1200
"""


def test_load_valid_csv_returns_dataset(tmp_path: Path) -> None:
    path = _write_csv(tmp_path, VALID_CSV)
    config = DataConfig(symbol="XAUUSD", timeframe="H1")

    dataset = load_dataset(path, config)

    assert dataset.metadata.symbol == "XAUUSD"
    assert dataset.metadata.timeframe == "H1"
    assert dataset.metadata.candle_count == 3
    assert dataset.metadata.integrity_status == "valid"
    assert len(dataset.candles) == 3
    assert dataset.candles[0].timestamp.tzinfo is not None
    assert dataset.candles[1].timestamp > dataset.candles[0].timestamp


def test_load_dataset_generates_version(tmp_path: Path) -> None:
    path = _write_csv(tmp_path, VALID_CSV)
    config = DataConfig(symbol="XAUUSD", timeframe="H1")

    dataset = load_dataset(path, config)

    assert dataset.metadata.dataset_version.startswith("XAUUSD_H1_2020_")
    assert dataset.metadata.dataset_version.endswith("_v001")


def test_load_missing_required_column_rejected(tmp_path: Path) -> None:
    content = "timestamp,open,high,low,close\n2020-01-01T00:00:00Z,1,2,0.5,1.5\n"
    path = _write_csv(tmp_path, content)
    config = DataConfig(symbol="XAUUSD", timeframe="H1")

    with pytest.raises(ValidationError, match="volume"):
        load_dataset(path, config)


def test_load_malformed_timestamp_rejected(tmp_path: Path) -> None:
    content = "timestamp,open,high,low,close,volume\nnot-a-date,1,2,0.5,1.5,10\n"
    path = _write_csv(tmp_path, content)
    config = DataConfig(symbol="XAUUSD", timeframe="H1")

    with pytest.raises(ValidationError, match="timestamp"):
        load_dataset(path, config)


def test_load_duplicate_timestamp_rejected(tmp_path: Path) -> None:
    content = (
        "timestamp,open,high,low,close,volume\n"
        "2020-01-01T00:00:00Z,1,2,0.5,1.5,10\n"
        "2020-01-01T00:00:00Z,1,2,0.5,1.5,10\n"
    )
    path = _write_csv(tmp_path, content)
    config = DataConfig(symbol="XAUUSD", timeframe="H1")

    with pytest.raises(ValidationError, match="duplicate"):
        load_dataset(path, config)


def test_load_unsorted_candle_rejected(tmp_path: Path) -> None:
    content = (
        "timestamp,open,high,low,close,volume\n"
        "2020-01-01T02:00:00Z,1,2,0.5,1.5,10\n"
        "2020-01-01T00:00:00Z,1,2,0.5,1.5,10\n"
    )
    path = _write_csv(tmp_path, content)
    config = DataConfig(symbol="XAUUSD", timeframe="H1")

    with pytest.raises(ValidationError, match="order|sorted|increasing"):
        load_dataset(path, config)


def test_load_invalid_ohlc_rejected(tmp_path: Path) -> None:
    content = "timestamp,open,high,low,close,volume\n2020-01-01T00:00:00Z,10,5,9,10,10\n"
    path = _write_csv(tmp_path, content)
    config = DataConfig(symbol="XAUUSD", timeframe="H1")

    with pytest.raises(ValidationError, match="high"):
        load_dataset(path, config)


def test_load_missing_value_rejected(tmp_path: Path) -> None:
    content = "timestamp,open,high,low,close,volume\n2020-01-01T00:00:00Z,10,11,,9.5,10\n"
    path = _write_csv(tmp_path, content)
    config = DataConfig(symbol="XAUUSD", timeframe="H1")

    with pytest.raises(ValidationError):
        load_dataset(path, config)


def test_load_file_not_found_rejected(tmp_path: Path) -> None:
    path = tmp_path / "does_not_exist.csv"
    config = DataConfig(symbol="XAUUSD", timeframe="H1")

    with pytest.raises(FileNotFoundError):
        load_dataset(path, config)
