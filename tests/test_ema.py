from __future__ import annotations

import math

import pytest

from mre.indicators.ema import ema


def test_ema_warmup_is_nan() -> None:
    closes = [1.0, 2.0, 3.0, 4.0, 5.0]
    result = ema(closes, period=3)
    assert len(result) == len(closes)
    assert all(math.isnan(v) for v in result[:2])
    assert not math.isnan(result[2])


def test_ema_first_valid_is_sma() -> None:
    closes = [1.0, 2.0, 3.0, 4.0, 5.0]
    result = ema(closes, period=3)
    assert math.isclose(result[2], (1.0 + 2.0 + 3.0) / 3.0)


def test_ema_reference_values() -> None:
    closes = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0]
    result = ema(closes, period=3)
    alpha = 2 / 4
    expected = [math.nan, math.nan, 2.0]
    for i in range(3, len(closes)):
        expected.append(alpha * closes[i] + (1 - alpha) * expected[i - 1])
    for got, want in zip(result, expected):
        if math.isnan(want):
            assert math.isnan(got)
        else:
            assert math.isclose(got, want, rel_tol=1e-9)


def test_ema_is_deterministic() -> None:
    closes = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0]
    assert ema(closes, period=3) == ema(closes, period=3)


def test_ema_no_lookahead() -> None:
    closes = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0]
    result = ema(closes, period=3)
    truncated = ema(closes[:5], period=3)
    for i in range(5):
        if math.isnan(result[i]):
            assert math.isnan(truncated[i])
        else:
            assert math.isclose(result[i], truncated[i], rel_tol=1e-9)


def test_ema_rejects_empty() -> None:
    with pytest.raises(ValueError):
        ema([], period=3)
