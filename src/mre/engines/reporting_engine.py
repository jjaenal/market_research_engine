"""Reporting Engine (ENG-007, ARC-006 §7.7)."""

from __future__ import annotations

from mre.models.report import Report, ReportConfig, ReportInput


def render(result: ReportInput, config: ReportConfig) -> Report:
    """Build an immutable Report from statistics, trades, and frozen config.

    Stateless and deterministic (Article 6, Article 7); the output is
    immutable once rendered (Article 13).
    """
    if result is None:
        raise ValueError("result is required")
    stats = result.statistics
    meta = result.dataset_metadata
    exec_cfg = result.execution

    dataset = {
        "symbol": meta.symbol,
        "timeframe": meta.timeframe,
        "timezone": meta.timezone,
        "source": meta.source,
        "dataset_version": meta.dataset_version,
        "date_range": f"{meta.date_range[0].isoformat()} .. {meta.date_range[1].isoformat()}",
        "candle_count": meta.candle_count,
        "integrity_status": meta.integrity_status,
    }

    configuration: dict = dict(config.strategy)
    configuration.update(
        {
            "position_size": exec_cfg.position_size,
            "commission_rate": exec_cfg.commission_rate,
            "slippage_rate": exec_cfg.slippage_rate,
            "hold_bars": exec_cfg.hold_bars,
            "stop_loss": exec_cfg.stop_loss,
            "take_profit": exec_cfg.take_profit,
        }
    )

    assumptions = {
        "entry": "next bar open",
        "exit": f"hold {exec_cfg.hold_bars} bars",
        "slippage": exec_cfg.slippage_rate,
        "transaction_cost": exec_cfg.commission_rate,
    }

    summary = {
        "trade_count": stats.trade_count,
        "net_pnl": stats.net_pnl,
        "win_rate": stats.win_rate,
        "profit_factor": stats.profit_factor,
        "expectancy": stats.expectancy,
        "max_drawdown": stats.max_drawdown,
    }

    experiment_metadata = {
        "experiment_id": config.experiment_id,
        "code_version": config.code_version,
        "generated_on": config.generated_on,
    }

    return Report(
        experiment_id=config.experiment_id,
        title=config.title,
        generated_on=config.generated_on,
        code_version=config.code_version,
        hypothesis=config.hypothesis,
        dataset=dataset,
        configuration=configuration,
        assumptions=assumptions,
        summary=summary,
        statistics=stats,
        trade_log=result.trades,
        equity_curve=stats.equity_curve,
        experiment_metadata=experiment_metadata,
        evidence_sufficient=stats.sufficient_sample,
        conclusion=config.conclusion,
    )
