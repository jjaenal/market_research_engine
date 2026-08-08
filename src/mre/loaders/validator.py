"""Data integrity validation (ARC-004 §8, FR-002)."""

from __future__ import annotations

from collections.abc import Sequence

from mre.models.candle import Candle


class ValidationError(ValueError):
    """Dataset failed one or more data integrity rules."""


def validate(candles: Sequence[Candle]) -> None:
    """Apply ARC-004 §8 integrity rules to an ordered candle sequence.

    Raises:
        ValidationError: on the first violation, with an explicit reason.
    """
    errors: list[str] = []

    prev_ts: Candle | None = None
    seen: set = set()
    for candle in candles:
        if candle.timestamp in seen:
            errors.append(f"duplicate timestamp: {candle.timestamp.isoformat()}")
            continue
        seen.add(candle.timestamp)

        if candle.open <= 0:
            errors.append(f"open must be > 0 (got {candle.open})")
        if candle.close <= 0:
            errors.append(f"close must be > 0 (got {candle.close})")
        if candle.high < max(candle.open, candle.close):
            errors.append(f"high must be >= max(open, close) (got {candle.high})")
        if candle.low > min(candle.open, candle.close):
            errors.append(f"low must be <= min(open, close) (got {candle.low})")
        if candle.volume < 0:
            errors.append(f"volume must be >= 0 (got {candle.volume})")

        if prev_ts is not None and candle.timestamp < prev_ts:
            errors.append(
                f"candles must be strictly increasing in time "
                f"({candle.timestamp.isoformat()} < {prev_ts.isoformat()})"
            )
        prev_ts = candle.timestamp

    if errors:
        raise ValidationError("; ".join(errors))
