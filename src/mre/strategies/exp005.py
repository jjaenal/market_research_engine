"""EXP-005 strategy — Price Breakout, Donchian-style (ENG-003 §10, ARC-008 ARC-ACT-010).

A pure price-momentum strategy distinct from the RSI Trendline Breakout
research line (EXP-001..EXP-004, closed): a LONG signal fires when a
price confirmation (close above the N-bar highest high — the Donchian
upper channel) is followed by a new swing-high fractal within the
confirmation window. No RSI/oscillator input; the strategy consumes only
existing Event types, so it registers as a plugin without any engine
change (ARC-ACT-010).
"""

from __future__ import annotations

from mre.models.event import PRICE_CONFIRMATION, SWING_HIGH
from mre.models.signal_rule import SignalRule
from mre.strategies.registry import register

PRICE_BREAKOUT_STRATEGY_ID = "price_breakout"


def exp005_signal_definition() -> tuple[SignalRule, ...]:
    """EXP-005 §9.3 signal definition (LONG momentum, Donchian-style)."""
    return (
        SignalRule(
            signal_type="LONG",
            trigger=PRICE_CONFIRMATION,
            confirmations=(SWING_HIGH,),
            window=5,
            source_strategy=PRICE_BREAKOUT_STRATEGY_ID,
        ),
    )


register(PRICE_BREAKOUT_STRATEGY_ID, exp005_signal_definition())
