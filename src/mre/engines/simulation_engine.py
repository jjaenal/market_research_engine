"""Simulation Engine (ENG-005, ARC-006 §7.5)."""

from __future__ import annotations

import math
from collections.abc import Sequence
from datetime import datetime

from mre.models.candle import Candle
from mre.models.execution import ExecutionConfig
from mre.models.order import Order
from mre.models.position import Position
from mre.models.signal import Signal
from mre.models.trade import Trade

_SIDES = {"LONG": "long", "SHORT": "short"}


def simulate(
    signals: Sequence[Signal],
    candles: Sequence[Candle],
    config: ExecutionConfig | None = None,
) -> tuple[Trade, ...]:
    """Simulate Trades from Signals using execution rules (ENG-005 §8).

    Entry occurs at the open of the candle after the Signal; exit is
    determined by SL (priority), TP, the scheduled ``hold_bars`` close,
    or the last available close when data is exhausted. No future
    information influences past execution (TODO-019).
    """
    cfg = config if config is not None else ExecutionConfig()
    if not candles:
        raise ValueError("candles must not be empty")

    index_of = {c.timestamp: i for i, c in enumerate(candles)}

    trades: list[Trade] = []
    for k, signal in enumerate(signals):
        side = _side(signal.signal_type)
        idx = index_of.get(signal.timestamp)
        if idx is None or idx + 1 >= len(candles):
            continue

        entry_bar = idx + 1
        entry_candle = candles[entry_bar]
        entry_price = _apply_slippage(entry_candle.open, side, entry=True, rate=cfg.slippage_rate)

        exit_bar, exit_raw = _find_exit(candles, entry_bar, side, cfg)
        exit_candle = candles[exit_bar]
        exit_price = _apply_slippage(exit_raw, side, entry=False, rate=cfg.slippage_rate)

        opened_at = entry_candle.timestamp
        closed_at = exit_candle.timestamp
        notional_entry = entry_price * cfg.position_size
        notional_exit = exit_price * cfg.position_size
        commission = cfg.commission_rate * (notional_entry + notional_exit)
        if side == "long":
            pnl = (exit_price - entry_price) * cfg.position_size - commission
        else:
            pnl = (entry_price - exit_price) * cfg.position_size - commission

        trades.append(
            Trade(
                trade_id=f"T-{k + 1:04d}",
                entry=Order(
                    order_type="market",
                    side=side,
                    price=entry_price,
                    trigger=entry_bar,
                    execution_status="executed",
                ),
                position=Position(
                    side=side,
                    entry_price=entry_price,
                    size=cfg.position_size,
                    opened_at=opened_at,
                    closed_at=closed_at,
                ),
                exit=Order(
                    order_type="market",
                    side=side,
                    price=exit_price,
                    trigger=exit_bar,
                    execution_status="executed",
                ),
                result=_classify(pnl),
                holding_period=closed_at - opened_at,
                pnl=pnl,
            )
        )

    return tuple(trades)


def _side(signal_type: str) -> str:
    if signal_type not in _SIDES:
        raise ValueError(f"unknown signal_type: {signal_type!r}")
    return _SIDES[signal_type]


def _apply_slippage(price: float, side: str, entry: bool, rate: float) -> float:
    if rate == 0.0:
        return price
    if side == "long":
        return price * (1.0 + rate) if entry else price * (1.0 - rate)
    return price * (1.0 - rate) if entry else price * (1.0 + rate)


def _find_exit(
    candles: Sequence[Candle],
    entry_bar: int,
    side: str,
    cfg: ExecutionConfig,
) -> tuple[int, float]:
    scheduled = entry_bar + cfg.hold_bars
    for j in range(entry_bar, len(candles)):
        c = candles[j]

        if cfg.stop_loss is not None:
            sl = cfg.stop_loss
            if side == "long":
                if c.open <= sl:
                    return j, c.open
                if c.low <= sl:
                    return j, sl
            else:
                if c.open >= sl:
                    return j, c.open
                if c.high >= sl:
                    return j, sl

        if cfg.take_profit is not None:
            tp = cfg.take_profit
            if side == "long":
                if c.open >= tp:
                    return j, c.open
                if c.high >= tp:
                    return j, tp
            else:
                if c.open <= tp:
                    return j, c.open
                if c.low <= tp:
                    return j, tp

        if j >= scheduled:
            return j, c.close

    last = len(candles) - 1
    return last, candles[last].close


def _classify(pnl: float) -> str:
    if math.isclose(pnl, 0.0, abs_tol=1e-9):
        return "BREAKEVEN"
    return "WIN" if pnl > 0 else "LOSS"
