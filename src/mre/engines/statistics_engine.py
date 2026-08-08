"""Statistics Engine (ENG-006, ARC-006 §7.6)."""

from __future__ import annotations

import math
from collections.abc import Sequence

from mre.models.statistics import StatisticsConfig, TradeStatistics
from mre.models.trade import Trade


def calculate(
    trades: Sequence[Trade],
    config: StatisticsConfig | None = None,
) -> TradeStatistics:
    """Compute the minimum statistics from a Trade ledger (RSH-004 §6).

    Win rate is the empirical win probability (initial research
    question: Probability). Average loss and gross loss use positive
    magnitudes. Metrics that are undefined for the input are None.
    """
    cfg = config if config is not None else StatisticsConfig()
    n = len(trades)

    wins = [t for t in trades if t.result == "WIN"]
    losses = [t for t in trades if t.result == "LOSS"]
    win_count = len(wins)
    loss_count = len(losses)

    gross_profit = sum(t.pnl for t in wins)
    gross_loss = sum(-t.pnl for t in losses)

    win_rate = win_count / n if n > 0 else None
    loss_rate = loss_count / n if n > 0 else None
    avg_win = gross_profit / win_count if win_count > 0 else None
    avg_loss = gross_loss / loss_count if loss_count > 0 else None
    risk_reward = avg_win / avg_loss if avg_win is not None and avg_loss else None
    net_pnl = gross_profit - gross_loss
    expectancy = net_pnl / n if n > 0 else None
    profit_factor = gross_profit / gross_loss if gross_loss > 0 else None

    returns = tuple(t.pnl for t in trades)
    mean_return = _mean(returns)
    std_return = _std(returns)
    skewness = _skewness(returns)

    equity = 0.0
    peak = 0.0
    max_drawdown = 0.0
    equity_curve: list[tuple] = []
    for t in trades:
        equity += t.pnl
        peak = max(peak, equity)
        max_drawdown = max(max_drawdown, peak - equity)
        equity_curve.append((t.position.closed_at, equity))

    return TradeStatistics(
        trade_count=n,
        win_count=win_count,
        loss_count=loss_count,
        win_rate=win_rate,
        loss_rate=loss_rate,
        avg_win=avg_win,
        avg_loss=avg_loss,
        risk_reward=risk_reward,
        expectancy=expectancy,
        profit_factor=profit_factor,
        gross_profit=gross_profit,
        gross_loss=gross_loss,
        net_pnl=net_pnl,
        max_drawdown=max_drawdown,
        winning_streak=_longest_streak(trades, "WIN"),
        losing_streak=_longest_streak(trades, "LOSS"),
        returns=returns,
        mean_return=mean_return,
        std_return=std_return,
        skewness=skewness,
        equity_curve=tuple(equity_curve),
        sufficient_sample=n >= cfg.min_sample,
    )


def _longest_streak(trades: Sequence[Trade], result: str) -> int:
    longest = 0
    current = 0
    for t in trades:
        if t.result == result:
            current += 1
            longest = max(longest, current)
        else:
            current = 0
    return longest


def _mean(values: tuple[float, ...]) -> float | None:
    if not values:
        return None
    return sum(values) / len(values)


def _std(values: tuple[float, ...]) -> float | None:
    mean = _mean(values)
    if mean is None:
        return None
    return math.sqrt(sum((v - mean) ** 2 for v in values) / len(values))


def _skewness(values: tuple[float, ...]) -> float | None:
    mean = _mean(values)
    if mean is None or len(values) < 3:
        return None
    m2 = sum((v - mean) ** 2 for v in values) / len(values)
    if m2 == 0:
        return None
    m3 = sum((v - mean) ** 3 for v in values) / len(values)
    return m3 / (m2 ** 1.5)
