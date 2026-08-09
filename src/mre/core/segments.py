"""Shared segment runner — run a frozen config on contiguous candle ranges (ARC-008 ARC-ACT-013)."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path

from mre.core.experiment_runner import ExperimentConfig, compute_report
from mre.loaders.normalize import RawCsvConfig, normalize_raw_csv
from mre.models.candle import Candle
from mre.models.statistics import TradeStatistics
from mre.utils.candle_csv import write_candle_csv


@dataclass(frozen=True)
class SegmentRun:
    """One contiguous candle-range run: its label and resulting statistics.

    Shared by out-of-sample (train/test) and robustness (period slices)
    so a labeled statistics result has one representation (ARC-008 ARC-ACT-013).
    """

    label: str
    statistics: TradeStatistics


def ensure_normalized(config: ExperimentConfig) -> Path:
    """Materialize the normalized dataset if missing and return its path.

    Both OOS and robustness reuse one normalized snapshot (Article 13);
    this folds the shared normalize-if-missing logic into one place.
    """
    if not config.normalized_dataset.exists():
        normalize_raw_csv(config.raw_dataset, config.normalized_dataset, RawCsvConfig())
    return config.normalized_dataset


def run_on_slice(
    config: ExperimentConfig,
    candles: Sequence[Candle],
    start: int,
    end: int,
    out_dir: Path,
    label: str,
) -> SegmentRun:
    """Write ``candles[start:end]`` to a compliant CSV and run the frozen config on it.

    RSH-003 §6/§7 (out-of-sample segments) and §10 (robustness period
    slices) both run the frozen config unchanged on a contiguous candle
    range; this unifies the ``write_candle_csv`` + ``compute_report``
    sequence they previously duplicated (ARC-008 ARC-ACT-013).

    The segment is written as ``XAUUSD_H1_{label}.csv`` under ``out_dir``
    and reloaded by ``compute_report`` (no lookahead, deterministic).
    """
    if not 0 <= start < end <= len(candles):
        raise ValueError(f"invalid candle slice ({start}, {end}) for {len(candles)} candles")
    path = write_candle_csv(candles[start:end], out_dir / f"XAUUSD_H1_{label}.csv")
    return SegmentRun(label=label, statistics=compute_report(config, path).statistics)
