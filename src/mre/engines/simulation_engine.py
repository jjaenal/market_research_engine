"""Simulation Engine (ENG-005, ARC-006 §7.5)."""

from __future__ import annotations

import math
from collections.abc import Sequence
from datetime import datetime

from mre.indicators.atr import atr
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

    Entry occurs at the open of the candle after the Signal is knowable:
    the later of (bar after the Signal timestamp) and (bar after every
    constituent Event's ``confirmable_ref``). This guarantees no same-bar
    or backdated entry even if a Signal's timestamp was constructed
    early (E-1, SPEC-003). Exit is determined by SL (priority), TP, the
    scheduled ``hold_bars`` close, or the last available close when data
    is exhausted. No future information influences past execution
    (TODO-019).
    """
    cfg = config if config is not None else ExecutionConfig()
    if not candles:
        raise ValueError("candles must not be empty")

    index_of = {c.timestamp: i for i, c in enumerate(candles)}

    atr_series = None
    if cfg.stop_loss_atr is not None or cfg.take_profit_atr is not None:
        atr_series = atr(candles, cfg.atr_period)

    trades: list[Trade] = []
    for k, signal in enumerate(signals):
        side = _side(signal.signal_type)
        idx = index_of.get(signal.timestamp)
        if idx is None or idx + 1 >= len(candles):
            continue

        entry_bar = max(idx + 1, _latest_confirmable_ref(signal) + 1)
        if entry_bar >= len(candles):
            continue
        entry_candle = candles[entry_bar]
        entry_price = _apply_slippage(entry_candle.open, side, entry=True, rate=cfg.slippage_rate)

        stop_level, take_level = _resolve_stop_take(entry_bar, entry_price, side, cfg, atr_series)
        exit_bar, exit_raw = _find_exit(candles, entry_bar, side, cfg, stop_level, take_level)
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


def _latest_confirmable_ref(signal: Signal) -> int:
    """Latest bar by which every constituent Event is knowable (SPEC-001).

    Returns -1 when no constituent Event carries a confirmable reference,
    so entry falls back to the Signal timestamp bar.
    """
    confirmable = [e.confirmable_ref for e in signal.events if e.confirmable_ref is not None]
    if not confirmable:
        return -1
    return max(confirmable)


def _apply_slippage(price: float, side: str, entry: bool, rate: float) -> float:
    if rate == 0.0:
        return price
    if side == "long":
        return price * (1.0 + rate) if entry else price * (1.0 - rate)
    return price * (1.0 - rate) if entry else price * (1.0 + rate)


def _resolve_stop_take(
    entry_bar: int,
    entry_price: float,
    side: str,
    cfg: ExecutionConfig,
    atr_series: Sequence[float] | None,
) -> tuple[float | None, float | None]:
    """Resolve SL/TP price levels for one trade.

    Absolute levels (``stop_loss``/``take_profit``) are used as given.
    ATR-multiple levels (RQ-007, ARC-008 §14.2) are anchored to the entry
    price using the ATR at the *last closed bar* ``entry_bar - 1`` (E-2,
    SPEC-004): ATR at the entry bar would use that bar's own OHLC — the
    entry-bar open, at which the levels must be set, is not yet complete.
    ``entry_bar >= 1`` always holds (entry happens at the earliest at bar
    1), so the anchor index is valid. ATR-multiple levels take precedence
    when both are configured. Warm-up (ATR is NaN) leaves the level unset
    (no SL/TP).
    """
    stop_level = cfg.stop_loss
    take_level = cfg.take_profit

    if atr_series is not None:
        atr_value = atr_series[entry_bar - 1]
        if not math.isnan(atr_value):
            if cfg.stop_loss_atr is not None:
                distance = cfg.stop_loss_atr * atr_value
                stop_level = entry_price - distance if side == "long" else entry_price + distance
            if cfg.take_profit_atr is not None:
                distance = cfg.take_profit_atr * atr_value
                take_level = entry_price + distance if side == "long" else entry_price - distance
    return stop_level, take_level


def _find_exit(
    candles: Sequence[Candle],
    entry_bar: int,
    side: str,
    cfg: ExecutionConfig,
    stop_level: float | None = None,
    take_level: float | None = None,
) -> tuple[int, float]:
    stop_level = cfg.stop_loss if stop_level is None else stop_level
    take_level = cfg.take_profit if take_level is None else take_level
    scheduled = entry_bar + cfg.hold_bars
    for j in range(entry_bar, len(candles)):
        c = candles[j]

        if stop_level is not None:
            sl = stop_level
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

        if take_level is not None:
            tp = take_level
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
