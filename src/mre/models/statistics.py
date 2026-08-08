"""Statistics result and configuration (ENG-006)."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class StatisticsConfig:
    """Statistics configuration (RSH-004 §7 sample requirements)."""

    min_sample: int = 30

    def __post_init__(self) -> None:
        if self.min_sample < 1:
            raise ValueError("min_sample must be >= 1")


@dataclass(frozen=True)
class TradeStatistics:
    """Immutable statistics result (ENG-006 §10, RSH-002 §8).

    Fields that are undefined for the given trades are None.
    """

    trade_count: int
    win_count: int
    loss_count: int
    win_rate: float | None
    loss_rate: float | None
    avg_win: float | None
    avg_loss: float | None
    risk_reward: float | None
    expectancy: float | None
    profit_factor: float | None
    gross_profit: float
    gross_loss: float
    net_pnl: float
    max_drawdown: float
    winning_streak: int
    losing_streak: int
    returns: tuple[float, ...]
    mean_return: float | None
    std_return: float | None
    skewness: float | None
    equity_curve: tuple[tuple[datetime, float], ...]
    sufficient_sample: bool
