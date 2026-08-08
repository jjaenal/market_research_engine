from __future__ import annotations

import dataclasses
from datetime import datetime, timezone

import pytest

from mre.models.statistics import TradeStatistics


def _ts(h: int) -> datetime:
    return datetime(2026, 1, 1, h, tzinfo=timezone.utc)


def test_statistics_holds_fields() -> None:
    stats = TradeStatistics(
        trade_count=3,
        win_count=2,
        loss_count=1,
        win_rate=2 / 3,
        loss_rate=1 / 3,
        avg_win=2.0,
        avg_loss=1.0,
        risk_reward=2.0,
        expectancy=1.0,
        profit_factor=4.0,
        gross_profit=4.0,
        gross_loss=1.0,
        net_pnl=3.0,
        max_drawdown=0.5,
        winning_streak=2,
        losing_streak=1,
        returns=(1.0, 3.0, -1.0),
        mean_return=1.0,
        std_return=1.0,
        skewness=0.0,
        equity_curve=((_ts(1), 1.0), (_ts(2), 4.0), (_ts(3), 3.0)),
        sufficient_sample=False,
    )
    assert stats.trade_count == 3
    assert stats.win_rate == pytest.approx(2 / 3)
    assert stats.expectancy == 1.0
    assert stats.returns == (1.0, 3.0, -1.0)
    assert stats.sufficient_sample is False


def test_statistics_is_frozen() -> None:
    stats = TradeStatistics(
        trade_count=0,
        win_count=0,
        loss_count=0,
        win_rate=None,
        loss_rate=None,
        avg_win=None,
        avg_loss=None,
        risk_reward=None,
        expectancy=None,
        profit_factor=None,
        gross_profit=0.0,
        gross_loss=0.0,
        net_pnl=0.0,
        max_drawdown=0.0,
        winning_streak=0,
        losing_streak=0,
        returns=(),
        mean_return=None,
        std_return=None,
        skewness=None,
        equity_curve=(),
        sufficient_sample=False,
    )
    with pytest.raises(dataclasses.FrozenInstanceError):
        stats.net_pnl = 5.0
