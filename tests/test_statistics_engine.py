from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest

from mre.engines.statistics_engine import calculate
from mre.models.order import Order
from mre.models.position import Position
from mre.models.statistics import StatisticsConfig
from mre.models.trade import Trade

_BASE = datetime(2026, 1, 1, tzinfo=timezone.utc)


def _ts(h: int) -> datetime:
    return _BASE + timedelta(hours=h)


def _trade(pnl: float, result: str, hour: int) -> Trade:
    ts = _ts(hour)
    price = 10.0 + pnl
    return Trade(
        trade_id=f"T-{hour:04d}",
        entry=Order(order_type="market", side="long", price=10.0, trigger=hour - 1, execution_status="executed"),
        position=Position(side="long", entry_price=10.0, size=1.0, opened_at=_ts(hour - 1), closed_at=ts),
        exit=Order(order_type="market", side="long", price=price, trigger=hour, execution_status="executed"),
        result=result,
        holding_period=ts - _ts(hour - 1),
        pnl=pnl,
    )


def _w(pnl: float, hour: int) -> Trade:
    return _trade(pnl, "WIN", hour)


def _l(pnl: float, hour: int) -> Trade:
    return _trade(pnl, "LOSS", hour)


def test_empty_trades() -> None:
    stats = calculate([])
    assert stats.trade_count == 0
    assert stats.win_rate is None
    assert stats.loss_rate is None
    assert stats.expectancy is None
    assert stats.profit_factor is None
    assert stats.max_drawdown == 0.0
    assert stats.winning_streak == 0
    assert stats.losing_streak == 0
    assert stats.returns == ()
    assert stats.equity_curve == ()
    assert stats.sufficient_sample is False


def test_all_wins() -> None:
    stats = calculate([_w(5.0, 1), _w(3.0, 2)])
    assert stats.trade_count == 2
    assert stats.win_count == 2
    assert stats.loss_count == 0
    assert stats.win_rate == pytest.approx(1.0)
    assert stats.loss_rate == pytest.approx(0.0)
    assert stats.avg_win == pytest.approx(4.0)
    assert stats.avg_loss is None
    assert stats.risk_reward is None
    assert stats.profit_factor is None
    assert stats.gross_profit == pytest.approx(8.0)
    assert stats.gross_loss == pytest.approx(0.0)
    assert stats.net_pnl == pytest.approx(8.0)
    assert stats.expectancy == pytest.approx(4.0)


def test_all_losses() -> None:
    stats = calculate([_l(-5.0, 1), _l(-3.0, 2)])
    assert stats.loss_rate == pytest.approx(1.0)
    assert stats.win_rate == pytest.approx(0.0)
    assert stats.avg_win is None
    assert stats.avg_loss == pytest.approx(4.0)
    assert stats.gross_loss == pytest.approx(8.0)
    assert stats.net_pnl == pytest.approx(-8.0)


def test_mixed_metrics() -> None:
    trades = [_w(4.0, 1), _l(-2.0, 2), _w(6.0, 3), _l(-2.0, 4)]
    stats = calculate(trades)
    assert stats.trade_count == 4
    assert stats.win_rate == pytest.approx(0.5)
    assert stats.loss_rate == pytest.approx(0.5)
    assert stats.avg_win == pytest.approx(5.0)
    assert stats.avg_loss == pytest.approx(2.0)
    assert stats.risk_reward == pytest.approx(2.5)
    assert stats.gross_profit == pytest.approx(10.0)
    assert stats.gross_loss == pytest.approx(4.0)
    assert stats.profit_factor == pytest.approx(2.5)
    assert stats.net_pnl == pytest.approx(6.0)
    assert stats.expectancy == pytest.approx(1.5)


def test_max_drawdown() -> None:
    trades = [_w(10.0, 1), _l(-20.0, 2), _w(5.0, 3), _w(10.0, 4)]
    stats = calculate(trades)
    assert stats.max_drawdown == pytest.approx(20.0)


def test_streaks() -> None:
    trades = [_w(1.0, 1), _w(1.0, 2), _l(-1.0, 3), _w(1.0, 4), _l(-1.0, 5), _l(-1.0, 6), _l(-1.0, 7)]
    stats = calculate(trades)
    assert stats.winning_streak == 2
    assert stats.losing_streak == 3


def test_equity_curve() -> None:
    trades = [_w(10.0, 1), _l(-4.0, 2)]
    stats = calculate(trades)
    assert stats.equity_curve == ((_ts(1), 10.0), (_ts(2), 6.0))


def test_distribution_stats() -> None:
    stats = calculate([_w(float(x), i) for i, x in enumerate([1, 2, 3, 4, 5], start=1)])
    assert stats.mean_return == pytest.approx(3.0)
    assert stats.std_return == pytest.approx((2.0) ** 0.5)
    assert stats.skewness == pytest.approx(0.0, abs=1e-9)


def test_positive_skewness() -> None:
    stats = calculate([_w(float(x), i) for i, x in enumerate([1, 1, 1, 1, 10], start=1)])
    assert stats.skewness is not None
    assert stats.skewness > 0


def test_sufficient_sample_threshold() -> None:
    enough = calculate([_w(1.0, i) for i in range(1, 31)])
    assert enough.sufficient_sample is True
    too_few = calculate([_w(1.0, i) for i in range(1, 30)])
    assert too_few.sufficient_sample is False


def test_custom_min_sample() -> None:
    config = StatisticsConfig(min_sample=5)
    stats = calculate([_w(1.0, i) for i in range(1, 6)], config)
    assert stats.sufficient_sample is True


def test_deterministic() -> None:
    trades = [_w(4.0, 1), _l(-2.0, 2), _w(6.0, 3)]
    assert calculate(trades) == calculate(trades)
