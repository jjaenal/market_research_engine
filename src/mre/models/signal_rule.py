"""Signal definition (ENG-003 §7)."""

from __future__ import annotations

import operator
from dataclasses import dataclass, field
from typing import Any, Mapping

_PAYLOAD_OPERATORS: Mapping[str, Any] = {
    "eq": operator.eq,
    "neq": operator.ne,
    "lt": operator.lt,
    "le": operator.le,
    "gt": operator.gt,
    "ge": operator.ge,
}


def _split_filter_key(key: str) -> tuple[str, str]:
    if "__" not in key:
        return key, "eq"
    field_name, op = key.split("__", 1)
    if not field_name:
        raise ValueError(f"invalid payload filter key: {key!r}")
    if op not in _PAYLOAD_OPERATORS:
        raise ValueError(f"unknown payload operator in filter key: {key!r}")
    return field_name, op


def payload_matches(payload: Any, filters: Mapping[str, Any]) -> bool:
    """Return True when ``payload`` satisfies every entry in ``filters``.

    Keys without an operator suffix (``"slope"``) are exact matches;
    keys with a suffix (``"slope__lt"``) use the named comparison.
    An empty filter matches any payload. A missing field never matches.
    """
    if not filters:
        return True
    if not isinstance(payload, dict):
        return False
    for key, expected in filters.items():
        field_name, op = _split_filter_key(key)
        if field_name not in payload:
            return False
        if not _PAYLOAD_OPERATORS[op](payload[field_name], expected):
            return False
    return True


@dataclass(frozen=True)
class SignalRule:
    """A deterministic Event combination rule (ENG-003 §7).

    A Signal fires when the trigger Event is followed by each required
    confirmation Event within ``window`` candle references. When
    ``trigger_payload`` is set, the trigger Event must also satisfy the
    declarative payload filter (e.g. ``{"slope__lt": 0.0}`` selects a
    specific break direction). Direction selection lives in the Signal
    Engine, not the detectors (ENG-002 §8).

    ``cooldown`` (default 0 = disabled) is the minimum number of candle
    references between consecutive Signals emitted by this rule
    (ARC-008 ARC-ACT-012). When enabled, after a Signal is emitted, any
    subsequent Signal whose reference is less than
    ``previous_reference + cooldown`` is suppressed — one decision per
    episode instead of one per trigger (avoids signal overlap, EXP-001 §15.3).
    """

    signal_type: str
    trigger: str
    confirmations: tuple[str, ...]
    window: int
    source_strategy: str = ""
    trigger_payload: Mapping[str, Any] = field(default_factory=dict)
    cooldown: int = 0

    def __post_init__(self) -> None:
        if not self.signal_type:
            raise ValueError("signal_type must not be empty")
        if not self.trigger:
            raise ValueError("trigger must not be empty")
        if not self.confirmations:
            raise ValueError("confirmations must not be empty")
        if len(set(self.confirmations)) != len(self.confirmations):
            raise ValueError("confirmations must not contain duplicates")
        if self.window < 1:
            raise ValueError("window must be >= 1")
        if self.cooldown < 0:
            raise ValueError("cooldown must be >= 0")
        for key in self.trigger_payload:
            if not isinstance(key, str):
                raise ValueError("trigger_payload keys must be strings")
            _split_filter_key(key)
