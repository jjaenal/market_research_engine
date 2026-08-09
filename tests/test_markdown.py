"""Shared Markdown helper tests (ARC-008 ARC-ACT-014)."""

from __future__ import annotations

import pytest

from mre.utils.markdown import heading, table


def test_heading_levels() -> None:
    assert heading(1, "T") == "# T"
    assert heading(2, "T") == "## T"
    assert heading(6, "T") == "###### T"


def test_heading_rejects_out_of_range() -> None:
    with pytest.raises(ValueError):
        heading(0, "T")
    with pytest.raises(ValueError):
        heading(7, "T")


def test_table_renders_header_separator_rows() -> None:
    md = table(["A", "B"], [["x", "1"], ["y", "2"]])
    assert md == "| A | B |\n| --- | --- |\n| x | 1 |\n| y | 2 |"


def test_table_empty_rows_still_renders_header() -> None:
    md = table(["A"], [])
    assert md == "| A |\n| --- |"


def test_table_deterministic() -> None:
    rows = [["b", "2"], ["a", "1"]]
    assert table(["K"], rows) == table(["K"], rows)
