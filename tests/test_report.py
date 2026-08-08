from __future__ import annotations

import dataclasses
from datetime import datetime, timedelta, timezone

import pytest

from mre.models.report import Report
from mre.models.statistics import TradeStatistics

_BASE = datetime(2026, 1, 1, tzinfo=timezone.utc)


def _ts(h: int) -> datetime:
    return _BASE + timedelta(hours=h)


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
        equity_curve=((_ts(1), 2.0),),
        sufficient_sample=False,
    )


def _report() -> Report:
    return Report(
        experiment_id="EXP-001",
        title="Baseline",
        generated_on="2026-08-08",
        code_version="abc123",
        hypothesis="Hipotesis.",
        dataset={"symbol": "XAUUSD"},
        configuration={"rsi_period": 14},
        assumptions={"entry": "next bar open"},
        summary={"net_pnl": 2.0},
        statistics=_stats(),
        trade_log=(),
        equity_curve=((_ts(1), 2.0),),
        experiment_metadata={"experiment_id": "EXP-001"},
        evidence_sufficient=False,
        conclusion="",
    )


def test_report_holds_fields() -> None:
    report = _report()
    assert report.experiment_id == "EXP-001"
    assert report.dataset == {"symbol": "XAUUSD"}
    assert report.equity_curve == ((_ts(1), 2.0),)
    assert report.evidence_sufficient is False


def test_report_is_frozen() -> None:
    report = _report()
    with pytest.raises(dataclasses.FrozenInstanceError):
        report.title = "X"


def test_markdown_contains_all_sections() -> None:
    markdown = _report().to_markdown()
    for section in [
        "## 1. Header",
        "## 2. Hypothesis",
        "## 3. Dataset",
        "## 4. Configuration",
        "## 5. Assumptions",
        "## 6. Summary",
        "## 7. Statistics",
        "## 8. Trade Log",
        "## 9. Equity Curve",
        "## 10. Experiment Metadata",
        "## 11. Evidence & Conclusion",
    ]:
        assert section in markdown


def test_markdown_renders_conclusion_area() -> None:
    report = dataclasses.replace(_report(), conclusion="Tidak ada edge.")
    markdown = report.to_markdown()
    assert "- Conclusion: Tidak ada edge." in markdown


def test_markdown_deterministic() -> None:
    report = _report()
    assert report.to_markdown() == report.to_markdown()
