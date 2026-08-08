"""Signal definition (ENG-003 §7)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SignalRule:
    """A deterministic Event combination rule (ENG-003 §7).

    A Signal fires when the trigger Event is followed by each required
    confirmation Event within ``window`` candle references.
    """

    signal_type: str
    trigger: str
    confirmations: tuple[str, ...]
    window: int
    source_strategy: str = ""

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
