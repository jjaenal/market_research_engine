"""EXP-007 strategy — Swing Breakout (Fractal Structure) (ENG-003 §10, ARC-008 ARC-ACT-010).

A LONG signal fires when a swing-high fractal (a structural resistance
level established by the swing detector, left/right = 2) is broken by a
price confirmation (close above the N-bar highest high) within the
confirmation window. Entry happens at the breakout candle — the price
confirmation, the latest constituent Event (FND-009 §13.5).

This is the structural complement of the Price Breakout strategy
(EXP-005, plugin `price_breakout`): there the Donchian-style breakout
comes first and the swing-high fractal confirms after; here the swing-high
fractal sets the level first and the price confirmation breaks it. The
strategy consumes only existing Event types (SWING_HIGH + PRICE_CONFIRMATION),
so it registers as a plugin without any engine change (ARC-ACT-010).
"""

from __future__ import annotations

from mre.models.event import PRICE_CONFIRMATION, SWING_HIGH
from mre.models.signal_rule import SignalRule
from mre.strategies.registry import register

SWING_BREAKOUT_STRATEGY_ID = "swing_breakout"


def exp007_signal_definition() -> tuple[SignalRule, ...]:
    """EXP-007 §9.3 signal definition (LONG fractal-structure swing breakout)."""
    return (
        SignalRule(
            signal_type="LONG",
            trigger=SWING_HIGH,
            confirmations=(PRICE_CONFIRMATION,),
            window=5,
            source_strategy=SWING_BREAKOUT_STRATEGY_ID,
        ),
    )


register(SWING_BREAKOUT_STRATEGY_ID, exp007_signal_definition())
