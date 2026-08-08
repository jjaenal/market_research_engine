from __future__ import annotations

import dataclasses

import pytest

from mre.models.report import ReportConfig


def test_report_config_defaults() -> None:
    config = ReportConfig(
        experiment_id="EXP-001",
        title="RSI Trendline Breakout Baseline",
        hypothesis="Breakout setelah konfirmasi harga memiliki keunggulan.",
        code_version="abc123",
    )
    assert config.strategy == {}
    assert config.conclusion == ""
    assert config.generated_on == ""


def test_report_config_holds_fields() -> None:
    config = ReportConfig(
        experiment_id="EXP-001",
        title="Baseline",
        hypothesis="H1",
        code_version="abc123",
        strategy={"rsi_period": 14},
        conclusion="Tidak ada edge.",
        generated_on="2026-08-08",
    )
    assert config.strategy == {"rsi_period": 14}
    assert config.conclusion == "Tidak ada edge."
    assert config.generated_on == "2026-08-08"


def test_report_config_is_frozen() -> None:
    config = ReportConfig(experiment_id="EXP-001", title="T", hypothesis="H", code_version="v1")
    with pytest.raises(dataclasses.FrozenInstanceError):
        config.title = "X"


def test_report_config_validation() -> None:
    with pytest.raises(ValueError):
        ReportConfig(experiment_id="", title="T", hypothesis="H", code_version="v1")
    with pytest.raises(ValueError):
        ReportConfig(experiment_id="EXP-001", title="", hypothesis="H", code_version="v1")
    with pytest.raises(ValueError):
        ReportConfig(experiment_id="EXP-001", title="T", hypothesis="", code_version="v1")
    with pytest.raises(ValueError):
        ReportConfig(experiment_id="EXP-001", title="T", hypothesis="H", code_version="")
