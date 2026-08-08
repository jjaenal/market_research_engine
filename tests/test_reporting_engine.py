from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest

from mre.engines.reporting_engine import render
from mre.engines.statistics_engine import calculate
from mre.models.dataset import DatasetMetadata
from mre.models.execution import ExecutionConfig
from mre.models.order import Order
from mre.models.position import Position
from mre.models.report import ReportConfig, ReportInput
from mre.models.trade import Trade

_BASE = datetime(2026, 1, 1, tzinfo=timezone.utc)


def _ts(h: int) -> datetime:
    return _BASE + timedelta(hours=h)


def _trade() -> Trade:
    opened = _ts(0)
    closed = _ts(1)
    return Trade(
        trade_id="T-0001",
        entry=Order(order_type="market", side="long", price=10.0, trigger=0, execution_status="executed"),
        position=Position(side="long", entry_price=10.0, size=1.0, opened_at=opened, closed_at=closed),
        exit=Order(order_type="market", side="long", price=12.0, trigger=1, execution_status="executed"),
        result="WIN",
        holding_period=closed - opened,
        pnl=2.0,
    )


def _meta() -> DatasetMetadata:
    return DatasetMetadata(
        dataset_version="1.0.0",
        symbol="XAUUSD",
        timeframe="H1",
        timezone="UTC",
        source="csv",
        date_range=(_ts(0), _ts(24)),
        candle_count=24,
        integrity_status="valid",
    )


def _config() -> ReportConfig:
    return ReportConfig(
        experiment_id="EXP-001",
        title="RSI Trendline Breakout Baseline",
        hypothesis="Breakout setelah konfirmasi harga memiliki keunggulan.",
        code_version="abc123",
        strategy={"rsi_period": 14},
        conclusion="",
        generated_on="2026-08-08",
    )


def _input() -> ReportInput:
    trade = _trade()
    return ReportInput(
        statistics=calculate([trade]),
        trades=(trade,),
        dataset_metadata=_meta(),
        execution=ExecutionConfig(),
    )


def test_render_populates_report() -> None:
    report = render(_input(), _config())
    assert report.experiment_id == "EXP-001"
    assert report.hypothesis == "Breakout setelah konfirmasi harga memiliki keunggulan."
    assert report.dataset["symbol"] == "XAUUSD"
    assert report.dataset["candle_count"] == 24
    assert report.configuration["rsi_period"] == 14
    assert report.configuration["hold_bars"] == 10
    assert report.assumptions["entry"] == "next bar open"
    assert report.summary["trade_count"] == 1
    assert report.statistics.trade_count == 1
    assert report.trade_log == (_trade(),)
    assert report.equity_curve == ((_ts(1), 2.0),)
    assert report.experiment_metadata["code_version"] == "abc123"
    assert report.evidence_sufficient is False


def test_render_evidence_sufficient() -> None:
    trades = tuple(_trade() for _ in range(30))
    inp = ReportInput(statistics=calculate(trades), trades=trades, dataset_metadata=_meta(), execution=ExecutionConfig())
    report = render(inp, _config())
    assert report.evidence_sufficient is True


def test_render_requires_result() -> None:
    with pytest.raises(ValueError):
        render(None, _config())  # type: ignore[arg-type]


def test_golden_markdown() -> None:
    report = render(_input(), _config())
    expected = """# MRE Experiment Report

## 1. Header

- Experiment ID: EXP-001
- Title: RSI Trendline Breakout Baseline
- Date: 2026-08-08
- Code Version: abc123

## 2. Hypothesis

Breakout setelah konfirmasi harga memiliki keunggulan.

## 3. Dataset

- Symbol: XAUUSD
- Timeframe: H1
- Timezone: UTC
- Source: csv
- Dataset Version: 1.0.0
- Date Range: 2026-01-01T00:00:00+00:00 .. 2026-01-02T00:00:00+00:00
- Candle Count: 24
- Integrity Status: valid

## 4. Configuration

- Rsi Period: 14
- Position Size: 1
- Commission Rate: 0
- Slippage Rate: 0
- Hold Bars: 10
- Stop Loss: -
- Take Profit: -

## 5. Assumptions

- Entry: next bar open
- Exit: hold 10 bars
- Slippage: 0
- Transaction Cost: 0

## 6. Summary

| Metric | Value |
| --- | --- |
| Trade Count | 1 |
| Net P&L | 2 |
| Win Rate | 1 |
| Profit Factor | - |
| Expectancy | 2 |
| Max Drawdown | 0 |

## 7. Statistics

| Metric | Value |
| --- | --- |
| Trade Count | 1 |
| Win Count | 1 |
| Loss Count | 0 |
| Win Rate | 1 |
| Loss Rate | 0 |
| Average Win | 2 |
| Average Loss | - |
| Risk Reward | - |
| Expectancy | 2 |
| Profit Factor | - |
| Gross Profit | 2 |
| Gross Loss | 0 |
| Net P&L | 2 |
| Max Drawdown | 0 |
| Winning Streak | 1 |
| Losing Streak | 0 |

## 8. Trade Log

| Trade ID | Side | Entry Time | Exit Time | Entry Price | Exit Price | Size | P&L | Result |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| T-0001 | long | 2026-01-01T00:00:00+00:00 | 2026-01-01T01:00:00+00:00 | 10 | 12 | 1 | 2 | WIN |

## 9. Equity Curve

```
2026-01-01T01:00:00+00:00,2
```

## 10. Experiment Metadata

- Experiment ID: EXP-001
- Code Version: abc123
- Generated On: 2026-08-08

## 11. Evidence & Conclusion

- Evidence Sufficient: false
- Conclusion: _(researcher)_

"""
    assert report.to_markdown() == expected
