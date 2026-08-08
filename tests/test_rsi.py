from __future__ import annotations

import math

import pytest

from mre.indicators.rsi import rsi


def _rsi_reference(closes: list[float], period: int) -> list[float]:
    result = [math.nan] * period
    deltas = [closes[i] - closes[i - 1] for i in range(1, len(closes))]
    avg_gain = sum(max(d, 0.0) for d in deltas[:period]) / period
    avg_loss = sum(max(-d, 0.0) for d in deltas[:period]) / period
    for i in range(period, len(closes)):
        gain = max(deltas[i - 1], 0.0)
        loss = max(-deltas[i - 1], 0.0)
        avg_gain = (avg_gain * (period - 1) + gain) / period
        avg_loss = (avg_loss * (period - 1) + loss) / period
        if avg_loss == 0:
            result.append(100.0)
        else:
            rs = avg_gain / avg_loss
            result.append(100.0 - 100.0 / (1.0 + rs))
    return result


def test_rsi_warmup_is_nan() -> None:
    closes = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0]
    result = rsi(closes, period=14)
    assert len(result) == len(closes)
    assert all(math.isnan(v) for v in result[:14])


def test_rsi_reference_values() -> None:
    closes = [44.34, 44.09, 44.15, 43.61, 44.33, 44.83, 45.10, 45.42, 45.84, 46.08, 45.89, 46.03, 45.61, 46.28, 46.28, 46.00]
    result = rsi(closes, period=14)
    expected = _rsi_reference(closes, period=14)
    for got, want in zip(result, expected):
        if math.isnan(want):
            assert math.isnan(got)
        else:
            assert math.isclose(got, want, rel_tol=1e-6)


def test_rsi_100_when_no_loss() -> None:
    closes = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0, 13.0, 14.0, 15.0]
    result = rsi(closes, period=14)
    assert math.isclose(result[14], 100.0)


def test_rsi_is_deterministic() -> None:
    closes = [44.34, 44.09, 44.15, 43.61, 44.33, 44.83, 45.10, 45.42, 45.84, 46.08, 45.89, 46.03, 45.61, 46.28, 46.28]
    assert rsi(closes, period=14) == rsi(closes, period=14)


def test_rsi_no_lookahead() -> None:
    closes = [44.34, 44.09, 44.15, 43.61, 44.33, 44.83, 45.10, 45.42, 45.84, 46.08, 45.89, 46.03, 45.61, 46.28, 46.28, 46.00]
    result = rsi(closes, period=14)
    truncated = rsi(closes[:15], period=14)
    for i in range(15):
        if math.isnan(result[i]):
            assert math.isnan(truncated[i])
        else:
            assert math.isclose(result[i], truncated[i], rel_tol=1e-9)


def test_rsi_rejects_empty() -> None:
    with pytest.raises(ValueError):
        rsi([], period=14)
