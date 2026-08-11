"""Compliant candle CSV serialization (ARC-004 §7 CSV contract)."""

from __future__ import annotations

import csv
from collections.abc import Sequence
from pathlib import Path

from mre.loaders.csv_loader import REQUIRED_COLUMNS
from mre.models.candle import Candle


def write_candle_csv(candles: Sequence[Candle], target: Path) -> Path:
    """Write candles as a compliant dataset CSV (header + ISO timestamps).

    The output matches the normalized contract so a written segment can be
    re-loaded by ``load_dataset`` (used by out-of-sample and robustness runs).
    Prices are serialized at full precision via ``repr`` so segment CSVs
    round-trip exactly (E-6, SPEC-005: no ``:g`` significant-digit rounding,
    which previously degraded OOS/robustness fidelity relative to baseline).
    Pure function: only reads ``candles``, only writes ``target``.
    """
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(list(REQUIRED_COLUMNS))
        for candle in candles:
            writer.writerow(
                [
                    candle.timestamp.isoformat(),
                    repr(candle.open),
                    repr(candle.high),
                    repr(candle.low),
                    repr(candle.close),
                    repr(candle.volume),
                ]
            )
    return target
