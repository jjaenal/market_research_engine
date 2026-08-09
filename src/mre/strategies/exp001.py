"""EXP-001 strategy — RSI Trendline Breakout (ENG-003 §10, ARC-008 ARC-ACT-010)."""

from __future__ import annotations

from mre.models.event import PRICE_CONFIRMATION, RSI_TRENDLINE_BROKEN
from mre.models.signal_rule import SignalRule
from mre.strategies.registry import register

EXP001_STRATEGY_ID = "rsi_trendline_breakout"


def exp001_signal_definition() -> tuple[SignalRule, ...]:
    """EXP-001 §9.3 signal definition (LONG baseline, ENG-003 §10)."""
    return (
        SignalRule(
            signal_type="LONG",
            trigger=RSI_TRENDLINE_BROKEN,
            confirmations=(PRICE_CONFIRMATION,),
            window=5,
            source_strategy=EXP001_STRATEGY_ID,
            trigger_payload={"slope__lt": 0.0},
        ),
    )


register(EXP001_STRATEGY_ID, exp001_signal_definition())
