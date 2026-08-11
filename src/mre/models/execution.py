"""Execution rules (ENG-005 §7, RSH-001 §14)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ExecutionConfig:
    """Simulation execution assumptions.

    Slippage is always conservative (worsens the price). TP/SL are
    optional execution rules; the MVP baseline experiment runs without
    them (PRD-006 §9). SL/TP may be given as absolute price levels
    (``stop_loss``/``take_profit``) or, for research iteration RQ-007
    (ARC-008 §14.2), as ATR multiples (``stop_loss_atr``/``take_profit_atr``)
    applied to the ATR at the *last closed bar* ``entry_bar - 1``
    (E-2, SPEC-004 — the entry bar's own OHLC is not yet complete when
    the levels are set). ATR-multiple levels take precedence when both
    are set.
    """

    position_size: float = 1.0
    commission_rate: float = 0.0
    slippage_rate: float = 0.0
    hold_bars: int = 10
    stop_loss: float | None = None
    take_profit: float | None = None
    stop_loss_atr: float | None = None
    take_profit_atr: float | None = None
    atr_period: int = 14

    def __post_init__(self) -> None:
        if self.position_size <= 0:
            raise ValueError("position_size must be > 0")
        if self.commission_rate < 0:
            raise ValueError("commission_rate must be >= 0")
        if self.slippage_rate < 0:
            raise ValueError("slippage_rate must be >= 0")
        if self.hold_bars < 1:
            raise ValueError("hold_bars must be >= 1")
        if self.stop_loss is not None and self.stop_loss <= 0:
            raise ValueError("stop_loss must be > 0")
        if self.take_profit is not None and self.take_profit <= 0:
            raise ValueError("take_profit must be > 0")
        if self.stop_loss_atr is not None and self.stop_loss_atr <= 0:
            raise ValueError("stop_loss_atr must be > 0")
        if self.take_profit_atr is not None and self.take_profit_atr <= 0:
            raise ValueError("take_profit_atr must be > 0")
        if self.atr_period < 1:
            raise ValueError("atr_period must be >= 1")
