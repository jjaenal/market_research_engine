from __future__ import annotations

import dataclasses
from datetime import datetime, timezone

import pytest

from mre.models.dataset import DatasetMetadata
from mre.models.execution import ExecutionConfig
from mre.models.order import Order
from mre.models.position import Position
from mre.models.report import ReportInput
from mre.models.statistics import TradeStatistics
from mre.models.trade import Trade


def _stats() -> TradeStatistics:
    return TradeStatistics(
        trade_count=1,
        win_count=1,
        loss_count=0,
        win_rate=1.0,
        loss_rate=0.0,
        avg_win=2.0,
        avg_loss=None,
        risk_reward=None,
        expectancy=2.0,
        profit_factor=None,
        gross_profit=2.0,
        gross_loss=0.0,
        net_pnl=2.0,
        max_drawdown=0.0,
        winning_streak=1,
        losing_streak=0,
        returns=(2.0,),
        mean_return=2.0,
        std_return=0.0,
        skewness=None,
        equity_curve=((datetime(2026, 1, 1, 1, tzinfo=timezone.utc), 2.0),),
        sufficient_sample=False,
    )


def _meta() -> DatasetMetadata:
    return DatasetMetadata(
        dataset_version="1.0.0",
        symbol="XAUUSD",
        timeframe="H1",
        timezone="UTC",
        source="csv",
        date_range=(datetime(2026, 1, 1, tzinfo=timezone.utc), datetime(2026, 1, 2, tzinfo=timezone.utc)),
        candle_count=24,
        integrity_status="valid",
    )


def test_report_input_holds_fields() -> None:
    entry = Order(order_type="market", side="long", price=10.0, trigger=0, execution_status="executed")
    exit = Order(order_type="market", side="long", price=12.0, trigger=1, execution_status="executed")
    position = Position(
        side="long",
        entry_price=10.0,
        size=1.0,
        opened_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
        closed_at=datetime(2026, 1, 1, 1, tzinfo=timezone.utc),
    )
    trade = Trade(
        trade_id="T-0001",
        entry=entry,
        position=position,
        exit=exit,
        result="WIN",
        holding_period=datetime(2026, 1, 1, 1, tzinfo=timezone.utc) - datetime(2026, 1, 1, tzinfo=timezone.utc),
        pnl=2.0,
    )
    inp = ReportInput(
        statistics=_stats(),
        trades=(trade,),
        dataset_metadata=_meta(),
        execution=ExecutionConfig(),
    )
    assert inp.statistics.trade_count == 1
    assert len(inp.trades) == 1
    assert inp.dataset_metadata.symbol == "XAUUSD"
    assert inp.execution.hold_bars == 10


def test_report_input_is_frozen() -> None:
    inp = ReportInput(statistics=_stats(), trades=(), dataset_metadata=_meta(), execution=ExecutionConfig())
    with pytest.raises(dataclasses.FrozenInstanceError):
        inp.trades = ()
