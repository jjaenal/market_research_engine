from __future__ import annotations

import math

from mre.core.experiment_runner import (
    ExperimentConfig,
    RegimeConfig,
    run_experiment,
    select_regime,
)
from mre.indicators.regime import HIGH, LOW, volatility_regime
from mre.models.candle import Candle
from mre.models.event import PRICE_CONFIRMATION, RSI_TRENDLINE_BROKEN
from mre.models.signal import Signal
from mre.models.signal_rule import SignalRule
from datetime import datetime, timedelta, timezone


def _write_raw(path, n: int = 400) -> None:
    lines: list[str] = []
    prev_close = 100.0
    for i in range(n):
        close = 100.0 + math.sin(i / 5.0) * 2.0
        open_ = prev_close
        high = max(open_, close) + 0.5
        low = min(open_, close) - 0.5
        hour = i % 24
        day = 1 + i // 24
        lines.append(
            f"2020-01-{day:02d} {hour:02d}:00,{open_:.3f},{high:.3f},{low:.3f},{close:.3f},10"
        )
        prev_close = close
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _config(tmp_path) -> ExperimentConfig:
    raw = tmp_path / "raw.csv"
    _write_raw(raw)
    return ExperimentConfig(
        experiment_id="EXP-001",
        title="RSI Trendline Breakout Baseline",
        hypothesis="Hipotesis.",
        code_version="test",
        generated_on="2026-08-08",
        strategy={"rsi_period": 14},
        raw_dataset=raw,
        normalized_dataset=tmp_path / "normalized.csv",
        report_path=tmp_path / "report.md",
        signal_definition=(
            SignalRule(
                signal_type="LONG",
                trigger=RSI_TRENDLINE_BROKEN,
                confirmations=(PRICE_CONFIRMATION,),
                window=5,
                source_strategy="rsi_trendline_breakout",
                trigger_payload={"slope__lt": 0.0},
            ),
        ),
    )


def test_run_experiment_produces_report(tmp_path) -> None:
    report = run_experiment(_config(tmp_path))

    assert report.experiment_id == "EXP-001"
    assert report.dataset["symbol"] == "XAUUSD"
    assert report.dataset["timeframe"] == "H1"
    assert report.configuration["rsi_period"] == 14
    assert report.configuration["hold_bars"] == 10
    assert report.experiment_metadata["code_version"] == "test"
    assert report.statistics.trade_count == len(report.trade_log)

    markdown = report.to_markdown()
    assert markdown.startswith("# MRE Experiment Report")
    for heading in (
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
    ):
        assert heading in markdown


def test_run_experiment_writes_artifacts(tmp_path) -> None:
    cfg = _config(tmp_path)
    run_experiment(cfg)

    assert cfg.normalized_dataset.exists()
    assert cfg.report_path.exists()
    rendered = cfg.report_path.read_text(encoding="utf-8")
    assert "Experiment ID: EXP-001" in rendered


def test_config_requires_signal_definition() -> None:
    import pytest

    with pytest.raises(ValueError):
        ExperimentConfig(
            experiment_id="EXP-001",
            title="T",
            hypothesis="H",
            code_version="v",
            generated_on="2026-08-08",
        )


def test_config_rejects_bad_regime() -> None:
    import pytest

    with pytest.raises(ValueError):
        RegimeConfig(selected_regime="medium")
    with pytest.raises(ValueError):
        RegimeConfig(atr_short_period=0)
    with pytest.raises(ValueError):
        RegimeConfig(atr_short_period=50, atr_long_period=20)


def test_config_applies_signal_cooldown(tmp_path) -> None:
    cfg = _config(tmp_path)
    assert all(rule.cooldown == 0 for rule in cfg.signal_definition)
    cfg = ExperimentConfig(**{**cfg.__dict__, "signal_cooldown": 5})
    assert all(rule.cooldown == 5 for rule in cfg.signal_definition)


def test_config_applies_signal_window(tmp_path) -> None:
    cfg = _config(tmp_path)
    assert all(rule.window == 5 for rule in cfg.signal_definition)
    cfg = ExperimentConfig(**{**cfg.__dict__, "signal_window": 7})
    assert all(rule.window == 7 for rule in cfg.signal_definition)


def test_config_rejects_negative_signal_window(tmp_path) -> None:
    import pytest

    with pytest.raises(ValueError):
        ExperimentConfig(**{**_config(tmp_path).__dict__, "signal_window": -1})


def _candle(idx: int, high: float, low: float) -> Candle:
    return Candle(
        timestamp=datetime(2020, 1, 1, tzinfo=timezone.utc) + timedelta(minutes=idx),
        open=(high + low) / 2,
        high=high,
        low=low,
        close=(high + low) / 2,
        volume=100.0,
    )


def test_select_regime_passthrough_when_off() -> None:
    candles = [_candle(i, 10, 9) for i in range(120)]
    signals = tuple(
        Signal(signal_type="LONG", timestamp=c.timestamp, events=()) for c in candles[:10]
    )
    out = select_regime(signals, candles, RegimeConfig(selected_regime=""))
    assert out == signals


def test_select_regime_filters_to_selected_label() -> None:
    candles = [
        _candle(i, 10 + (i % 7), 9) for i in range(160)
    ]
    labels = volatility_regime(candles, 14, 100)
    signals = tuple(
        Signal(signal_type="LONG", timestamp=c.timestamp, events=()) for c in candles
    )
    for selected in ("high", "low"):
        out = select_regime(signals, candles, RegimeConfig(selected_regime=selected))
        expected = [s for s, label in zip(signals, labels) if label == selected]
        assert out == tuple(expected)


def test_select_regime_drops_warmup_signals() -> None:
    candles = [_candle(i, 10, 9) for i in range(80)]
    signals = tuple(
        Signal(signal_type="LONG", timestamp=c.timestamp, events=()) for c in candles
    )
    out = select_regime(signals, candles, RegimeConfig(selected_regime="high"))
    assert len(out) == 0


def _regime_config(tmp_path, selected: str = "") -> ExperimentConfig:
    cfg = _config(tmp_path)
    return ExperimentConfig(
        **{**cfg.__dict__, "regime_config": RegimeConfig(selected_regime=selected)}
    )


def test_run_experiment_with_regime_filter(tmp_path) -> None:
    report_off = run_experiment(_regime_config(tmp_path, selected=""))
    report_on = run_experiment(_regime_config(tmp_path, selected="high"))
    assert report_off.statistics.trade_count >= report_on.statistics.trade_count
