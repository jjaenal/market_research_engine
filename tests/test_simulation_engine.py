from __future__ import annotations

from datetime import datetime, timezone

import pytest

from mre.engines.simulation_engine import simulate
from mre.models.candle import Candle
from mre.models.event import Event
from mre.models.execution import ExecutionConfig
from mre.models.signal import Signal


def _ts(h: int) -> datetime:
    return datetime(2026, 1, 1, h, tzinfo=timezone.utc)


def _candles(closes: list[float]) -> tuple[Candle, ...]:
    candles: list[Candle] = []
    for i, c in enumerate(closes):
        prev = closes[i - 1] if i > 0 else c
        candles.append(
            Candle(
                timestamp=_ts(i),
                open=prev,
                high=max(prev, c),
                low=min(prev, c),
                close=c,
                volume=0.0,
            )
        )
    return tuple(candles)


def _signal(signal_type: str, hour: int) -> Signal:
    return Signal(signal_type=signal_type, timestamp=_ts(hour), events=())


def _event(confirmable_ref: int) -> Event:
    return Event(
        event_type="SWING_HIGH",
        timestamp=_ts(0),
        source_detector="test",
        reference=0,
        payload={},
        confirmable_ref=confirmable_ref,
    )


def _cfg(**kwargs) -> ExecutionConfig:
    return ExecutionConfig(**kwargs)


def test_bar_exit_long_win() -> None:
    closes = [10.0, 10.0, 11.0, 12.0, 13.0, 14.0, 14.0, 14.0]
    trades = simulate([_signal("LONG", 0)], _candles(closes), _cfg(hold_bars=3))
    assert len(trades) == 1
    (trade,) = trades
    assert trade.trade_id == "T-0001"
    assert trade.entry.price == 10.0
    assert trade.exit.price == 13.0
    assert trade.position.opened_at == _ts(1)
    assert trade.position.closed_at == _ts(4)
    assert trade.pnl == pytest.approx(3.0)
    assert trade.result == "WIN"
    assert trade.holding_period == _ts(4) - _ts(1)


def test_slippage_and_commission() -> None:
    closes = [10.0, 10.0, 11.0, 12.0, 13.0, 14.0, 14.0, 14.0]
    trades = simulate(
        [_signal("LONG", 0)],
        _candles(closes),
        _cfg(hold_bars=3, commission_rate=0.001, slippage_rate=0.001),
    )
    (trade,) = trades
    entry = 10.0 * 1.001
    exit = 13.0 * 0.999
    gross = (exit - entry) * 1.0
    commission = 0.001 * (entry + exit)
    assert trade.pnl == pytest.approx(gross - commission)


def test_signal_at_last_bar_is_skipped() -> None:
    closes = [10.0, 10.0, 11.0, 12.0, 13.0]
    trades = simulate([_signal("LONG", 4)], _candles(closes), _cfg(hold_bars=3))
    assert trades == ()


def test_no_signals() -> None:
    closes = [10.0, 10.0, 11.0, 12.0, 13.0]
    assert simulate([], _candles(closes), _cfg(hold_bars=3)) == ()


def test_short_position() -> None:
    closes = [10.0, 10.0, 11.0, 12.0, 13.0, 14.0]
    trades = simulate([_signal("SHORT", 0)], _candles(closes), _cfg(hold_bars=3))
    (trade,) = trades
    assert trade.position.side == "short"
    assert trade.entry.price == 10.0
    assert trade.exit.price == 13.0
    assert trade.pnl == pytest.approx(-3.0)
    assert trade.result == "LOSS"


def test_stop_loss_triggers_early() -> None:
    closes = [10.0, 10.0, 12.0, 11.0, 9.0, 8.0]
    trades = simulate([_signal("LONG", 0)], _candles(closes), _cfg(hold_bars=10, stop_loss=9.0))
    (trade,) = trades
    assert trade.exit.price == 9.0
    assert trade.position.closed_at == _ts(4)
    assert trade.pnl == pytest.approx(-1.0)
    assert trade.result == "LOSS"


def test_take_profit_triggers_early() -> None:
    closes = [10.0, 10.0, 12.0, 14.0, 15.0]
    trades = simulate([_signal("LONG", 0)], _candles(closes), _cfg(hold_bars=10, take_profit=12.0))
    (trade,) = trades
    assert trade.exit.price == 12.0
    assert trade.pnl == pytest.approx(2.0)
    assert trade.result == "WIN"


def test_sl_priority_over_tp_same_bar() -> None:
    candle1 = Candle(timestamp=_ts(1), open=10.0, high=14.0, low=8.0, close=12.0, volume=0.0)
    candles = (Candle(timestamp=_ts(0), open=10.0, high=10.0, low=10.0, close=10.0, volume=0.0), candle1)
    trades = simulate(
        [_signal("LONG", 0)],
        candles,
        _cfg(hold_bars=10, stop_loss=9.0, take_profit=12.0),
    )
    (trade,) = trades
    assert trade.exit.price == 9.0
    assert trade.result == "LOSS"


def test_gap_beyond_sl_exits_at_open() -> None:
    candle1 = Candle(timestamp=_ts(1), open=8.0, high=8.0, low=7.0, close=7.0, volume=0.0)
    candles = (Candle(timestamp=_ts(0), open=10.0, high=10.0, low=10.0, close=10.0, volume=0.0), candle1)
    trades = simulate([_signal("LONG", 0)], candles, _cfg(hold_bars=10, stop_loss=9.0))
    (trade,) = trades
    assert trade.exit.price == 8.0


def test_data_exhaustion_exits_at_last_close() -> None:
    closes = [10.0, 10.0, 12.0, 14.0]
    trades = simulate([_signal("LONG", 0)], _candles(closes), _cfg(hold_bars=10))
    (trade,) = trades
    assert trade.exit.price == 14.0
    assert trade.pnl == pytest.approx(4.0)


def test_stop_loss_atr_anchored_to_entry() -> None:
    closes = [10.0, 10.0, 12.0, 11.0, 9.0, 8.0, 8.0, 8.0]
    trades = simulate(
        [_signal("LONG", 0)],
        _candles(closes),
        _cfg(hold_bars=10, stop_loss_atr=1.0, atr_period=5),
    )
    (trade,) = trades
    assert trade.exit.price < 10.0
    assert trade.result == "LOSS"
    assert trade.position.closed_at < _ts(4) or trade.exit.price < 9.0


def test_take_profit_atr_anchored_to_entry() -> None:
    closes = [10.0, 10.0, 12.0, 13.0, 14.0, 15.0, 15.0, 15.0]
    trades = simulate(
        [_signal("LONG", 0)],
        _candles(closes),
        _cfg(hold_bars=10, take_profit_atr=1.0, atr_period=5),
    )
    (trade,) = trades
    assert trade.exit.price > 10.0
    assert trade.result == "WIN"


def test_atr_sl_tp_precedence_over_absolute() -> None:
    closes = [10.0, 10.2, 10.1, 10.3, 10.2, 10.0, 8.5, 8.0, 8.0, 8.0]
    absolute_only = simulate(
        [_signal("LONG", 4)], _candles(closes), _cfg(hold_bars=10, stop_loss=8.0)
    )
    with_atr = simulate(
        [_signal("LONG", 4)],
        _candles(closes),
        _cfg(hold_bars=10, stop_loss=8.0, stop_loss_atr=1.0, atr_period=4),
    )
    (a,) = absolute_only
    (b,) = with_atr
    assert b.exit.price != a.exit.price  # ATR level used, not the absolute 8.0


def test_atr_sl_tp_warmup_skipped() -> None:
    closes = [10.0, 10.0, 12.0, 14.0]
    trades = simulate(
        [_signal("LONG", 0)],
        _candles(closes),
        _cfg(hold_bars=10, stop_loss_atr=1.0, atr_period=100),
    )
    (trade,) = trades
    assert trade.exit.price == 14.0  # hold_bars path, no SL triggered


def test_atr_sl_tp_deterministic() -> None:
    closes = [10.0, 10.0, 12.0, 11.0, 9.0, 8.0, 9.0, 10.0]
    cfg = _cfg(hold_bars=5, stop_loss_atr=2.0, take_profit_atr=3.0, atr_period=5)
    a = simulate([_signal("LONG", 0)], _candles(closes), cfg)
    b = simulate([_signal("LONG", 0)], _candles(closes), cfg)
    assert a == b


def test_no_future_information() -> None:
    closes = [10.0, 10.0, 11.0, 12.0, 13.0, 14.0, 15.0, 16.0]
    cfg = _cfg(hold_bars=3)
    full = simulate([_signal("LONG", 0)], _candles(closes), cfg)
    truncated = simulate([_signal("LONG", 0)], _candles(closes[:6]), cfg)
    assert full == truncated


def test_deterministic() -> None:
    closes = [10.0, 10.0, 11.0, 12.0, 13.0, 14.0]
    cfg = _cfg(hold_bars=3, commission_rate=0.001, slippage_rate=0.001)
    a = simulate([_signal("LONG", 0)], _candles(closes), cfg)
    b = simulate([_signal("LONG", 0)], _candles(closes), cfg)
    assert a == b


def test_multiple_signals_produce_independent_trades() -> None:
    closes = [10.0, 10.0, 11.0, 12.0, 13.0, 14.0, 14.0, 15.0]
    trades = simulate(
        [_signal("LONG", 0), _signal("LONG", 4)],
        _candles(closes),
        _cfg(hold_bars=2),
    )
    assert [t.trade_id for t in trades] == ["T-0001", "T-0002"]


def test_unknown_signal_type_raises() -> None:
    closes = [10.0, 10.0, 11.0, 12.0]
    with pytest.raises(ValueError):
        simulate([_signal("HOLD", 0)], _candles(closes), _cfg(hold_bars=2))


def test_no_signal_timestamp_skipped() -> None:
    closes = [10.0, 10.0, 11.0, 12.0]
    missing = Signal(signal_type="LONG", timestamp=datetime(2026, 1, 2, 0, tzinfo=timezone.utc), events=())
    assert simulate([missing], _candles(closes), _cfg(hold_bars=2)) == ()


def test_entry_after_confirmable_ref() -> None:
    closes = [10.0, 10.0, 11.0, 12.0, 13.0, 14.0]
    signal = Signal(
        signal_type="LONG",
        timestamp=_ts(0),
        events=(_event(confirmable_ref=2),),
    )
    trades = simulate([signal], _candles(closes), _cfg(hold_bars=3))
    assert len(trades) == 1
    (trade,) = trades
    assert trade.entry.trigger == 3
    assert trade.entry.price == 11.0
    assert trade.position.opened_at == _ts(3)


def test_entry_after_confirmable_ref_mixed_with_plain_events() -> None:
    closes = [10.0, 10.0, 11.0, 12.0, 13.0, 14.0]
    signal = Signal(
        signal_type="LONG",
        timestamp=_ts(0),
        events=(_event(confirmable_ref=2), Event(
            event_type="PRICE_CONFIRMATION",
            timestamp=_ts(0),
            source_detector="test",
            reference=0,
            payload={},
        )),
    )
    trades = simulate([signal], _candles(closes), _cfg(hold_bars=3))
    assert len(trades) == 1
    (trade,) = trades
    assert trade.entry.trigger == 3


def test_entry_uses_latest_of_timestamp_and_confirmable_ref() -> None:
    closes = [10.0, 10.0, 11.0, 12.0, 13.0, 14.0]
    signal = Signal(
        signal_type="LONG",
        timestamp=_ts(3),
        events=(_event(confirmable_ref=1),),
    )
    trades = simulate([signal], _candles(closes), _cfg(hold_bars=3))
    assert len(trades) == 1
    (trade,) = trades
    assert trade.entry.trigger == 4


def test_signal_skipped_when_confirmable_ref_at_last_bar() -> None:
    closes = [10.0, 10.0, 11.0, 12.0, 13.0]
    signal = Signal(
        signal_type="LONG",
        timestamp=_ts(0),
        events=(_event(confirmable_ref=4),),
    )
    assert simulate([signal], _candles(closes), _cfg(hold_bars=3)) == ()
