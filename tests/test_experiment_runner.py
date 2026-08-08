from __future__ import annotations

import math

from mre.core.experiment_runner import ExperimentConfig, run_experiment
from mre.models.event import PRICE_CONFIRMATION, RSI_TRENDLINE_BROKEN
from mre.models.signal_rule import SignalRule


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
