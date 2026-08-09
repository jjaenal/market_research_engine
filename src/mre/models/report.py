"""Report models (ENG-007)."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from mre.models.dataset import DatasetMetadata
from mre.models.execution import ExecutionConfig
from mre.models.statistics import TradeStatistics
from mre.models.trade import Trade
from mre.utils.markdown import heading, table


@dataclass(frozen=True)
class ReportConfig:
    """Frozen experiment configuration for the report (PRD-003 §7.3)."""

    experiment_id: str
    title: str
    hypothesis: str
    code_version: str
    strategy: dict[str, Any] = field(default_factory=dict)
    conclusion: str = ""
    generated_on: str = ""

    def __post_init__(self) -> None:
        if not self.experiment_id:
            raise ValueError("experiment_id must not be empty")
        if not self.title:
            raise ValueError("title must not be empty")
        if not self.hypothesis:
            raise ValueError("hypothesis must not be empty")
        if not self.code_version:
            raise ValueError("code_version must not be empty")


@dataclass(frozen=True)
class ReportInput:
    """`result` for ReportingEngine.render (ARC-006 §7.7)."""

    statistics: TradeStatistics
    trades: tuple[Trade, ...]
    dataset_metadata: DatasetMetadata
    execution: ExecutionConfig


@dataclass(frozen=True)
class Report:
    """Immutable structured report (Article 13, ENG-007 §6)."""

    experiment_id: str
    title: str
    generated_on: str
    code_version: str
    hypothesis: str
    dataset: dict[str, Any]
    configuration: dict[str, Any]
    assumptions: dict[str, Any]
    summary: dict[str, Any]
    statistics: TradeStatistics
    trade_log: tuple[Trade, ...]
    equity_curve: tuple[tuple[datetime, float], ...]
    experiment_metadata: dict[str, Any]
    evidence_sufficient: bool
    conclusion: str

    def to_markdown(self) -> str:
        """Render the report as deterministic Markdown (ENG-007 §9)."""
        lines: list[str] = []
        lines.append(heading(1, "MRE Experiment Report"))
        lines.append("")

        lines.append(heading(2, "1. Header"))
        lines.append("")
        lines.append(f"- Experiment ID: {self.experiment_id}")
        lines.append(f"- Title: {self.title}")
        lines.append(f"- Date: {self.generated_on or '-'}")
        lines.append(f"- Code Version: {self.code_version}")
        lines.append("")

        lines.append(heading(2, "2. Hypothesis"))
        lines.append("")
        lines.append(self.hypothesis)
        lines.append("")

        lines.append(heading(2, "3. Dataset"))
        lines.append("")
        _kv_lines(lines, self.dataset)
        lines.append("")

        lines.append(heading(2, "4. Configuration"))
        lines.append("")
        _kv_lines(lines, self.configuration)
        lines.append("")

        lines.append(heading(2, "5. Assumptions"))
        lines.append("")
        _kv_lines(lines, self.assumptions)
        lines.append("")

        lines.append(heading(2, "6. Summary"))
        lines.append("")
        _table(lines, self.summary)
        lines.append("")

        lines.append(heading(2, "7. Statistics"))
        lines.append("")
        _table(lines, _statistics_rows(self.statistics))
        lines.append("")

        lines.append(heading(2, "8. Trade Log"))
        lines.append("")
        _trade_log(lines, self.trade_log)
        lines.append("")

        lines.append(heading(2, "9. Equity Curve"))
        lines.append("")
        lines.append("```")
        for ts, equity in self.equity_curve:
            lines.append(f"{ts.isoformat()},{_fmt(equity)}")
        lines.append("```")
        lines.append("")

        lines.append(heading(2, "10. Experiment Metadata"))
        lines.append("")
        _kv_lines(lines, self.experiment_metadata)
        lines.append("")

        lines.append(heading(2, "11. Evidence & Conclusion"))
        lines.append("")
        lines.append(f"- Evidence Sufficient: {str(self.evidence_sufficient).lower()}")
        if self.conclusion:
            lines.append(f"- Conclusion: {self.conclusion}")
        else:
            lines.append("- Conclusion: _(researcher)_")
        lines.append("")

        return "\n".join(lines) + "\n"


def _fmt(value: Any) -> str:
    if value is None:
        return "-"
    if isinstance(value, (int, float)):
        return f"{value:g}"
    return str(value)


def _kv_lines(lines: list[str], mapping: dict[str, Any]) -> None:
    for key, value in mapping.items():
        lines.append(f"- {_label(key)}: {_fmt(value)}")


def _table(lines: list[str], mapping: dict[str, Any]) -> None:
    rows = [[_label(key), _fmt(value)] for key, value in mapping.items()]
    lines.append(table(["Metric", "Value"], rows))


_P_AND_L = "Net P&L"


def _label(key: str) -> str:
    special = {"net_pnl": _P_AND_L, "experiment_id": "Experiment ID"}
    if key in special:
        return special[key]
    return " ".join(word.capitalize() for word in key.split("_"))


def _statistics_rows(stats: TradeStatistics) -> dict[str, Any]:
    return {
        "trade_count": stats.trade_count,
        "win_count": stats.win_count,
        "loss_count": stats.loss_count,
        "win_rate": stats.win_rate,
        "loss_rate": stats.loss_rate,
        "average_win": stats.avg_win,
        "average_loss": stats.avg_loss,
        "risk_reward": stats.risk_reward,
        "expectancy": stats.expectancy,
        "profit_factor": stats.profit_factor,
        "gross_profit": stats.gross_profit,
        "gross_loss": stats.gross_loss,
        "net_pnl": stats.net_pnl,
        "max_drawdown": stats.max_drawdown,
        "winning_streak": stats.winning_streak,
        "losing_streak": stats.losing_streak,
    }


def _trade_log(lines: list[str], trades: tuple[Trade, ...]) -> None:
    headers = ["Trade ID", "Side", "Entry Time", "Exit Time", "Entry Price", "Exit Price", "Size", "P&L", "Result"]
    rows = [
        [
            t.trade_id,
            t.position.side,
            t.position.opened_at.isoformat(),
            t.position.closed_at.isoformat() if t.position.closed_at else "-",
            _fmt(t.position.entry_price),
            _fmt(t.exit.price),
            _fmt(t.position.size),
            _fmt(t.pnl),
            t.result,
        ]
        for t in trades
    ]
    lines.append(table(headers, rows))
