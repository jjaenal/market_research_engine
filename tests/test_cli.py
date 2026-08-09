"""Unified experiment CLI tests (ARC-008 ARC-ACT-014)."""

from __future__ import annotations

import dataclasses
import math
from pathlib import Path

import pytest

from mre.cli import main as cli_main
from mre.core.experiment_runner import exp001_config, main as baseline_main
from mre.core.sensitivity import main as sensitivity_main


def _write_raw(path: Path, n: int = 400) -> None:
    lines: list[str] = []
    prev_close = 100.0
    for i in range(n):
        seg = i // 40
        level = float(seg * 4)
        if seg % 2 == 0:
            close = 100.0 + level + math.sin(i / 4.0) * 3.0
        else:
            close = 100.0 + level + math.sin(i / 2.0) * 1.0
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


def _monkeypatch_config(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> Path:
    raw = tmp_path / "raw.csv"
    _write_raw(raw)

    def build(out: Path, *, source: Path = Path("datasets/XAUUSD_H1.csv"), **_: object):
        cfg = exp001_config(out, source=source)
        return dataclasses.replace(
            cfg,
            raw_dataset=source,
            normalized_dataset=tmp_path / "normalized.csv",
        )

    monkeypatch.setattr("mre.cli.exp001_config", build)
    return raw


def test_exp001_config_is_single_builder(tmp_path: Path) -> None:
    cfg = exp001_config(tmp_path / "report.md", source=tmp_path / "raw.csv")
    assert cfg.experiment_id == "EXP-001"
    assert cfg.strategy["rsi_period"] == 14
    assert cfg.signal_definition
    assert cfg.raw_dataset == tmp_path / "raw.csv"
    assert cfg.report_path == tmp_path / "report.md"


def test_baseline_subcommand_writes_report(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    raw = _monkeypatch_config(monkeypatch, tmp_path)
    out = tmp_path / "report.md"
    assert cli_main(["baseline", "--source", str(raw), "--out", str(out)]) == 0
    assert out.exists()
    assert "EXP-001" in out.read_text(encoding="utf-8")


def test_sensitivity_subcommand_writes_report(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    raw = _monkeypatch_config(monkeypatch, tmp_path)
    out = tmp_path / "sens.md"
    assert cli_main(["sensitivity", "--source", str(raw), "--out", str(out)]) == 0
    assert out.exists()
    assert "Sensitivity Analysis" in out.read_text(encoding="utf-8")


def test_oos_subcommand_writes_report(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    raw = _monkeypatch_config(monkeypatch, tmp_path)
    out = tmp_path / "oos.md"
    assert cli_main(["oos", "--source", str(raw), "--out", str(out), "--split", "0.5"]) == 0
    assert out.exists()
    assert "Out-of-Sample Testing" in out.read_text(encoding="utf-8")


def test_robustness_subcommand_writes_report(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    raw = _monkeypatch_config(monkeypatch, tmp_path)
    out = tmp_path / "rob.md"
    assert cli_main(["robustness", "--source", str(raw), "--out", str(out), "--no-market"]) == 0
    assert out.exists()
    assert "Robustness Analysis" in out.read_text(encoding="utf-8")


def test_unknown_subcommand_rejected(tmp_path: Path) -> None:
    with pytest.raises(SystemExit):
        cli_main(["nope"])


def test_module_mains_delegate_to_cli(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    raw = _monkeypatch_config(monkeypatch, tmp_path)
    report_out = tmp_path / "report.md"
    sens_out = tmp_path / "sens.md"
    assert baseline_main(["--source", str(raw), "--out", str(report_out)]) == 0
    assert sensitivity_main(["--source", str(raw), "--out", str(sens_out)]) == 0
    assert report_out.exists() and sens_out.exists()
