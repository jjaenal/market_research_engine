"""Shared Markdown rendering helpers (ARC-008 ARC-ACT-014)."""

from __future__ import annotations

from collections.abc import Sequence


def heading(level: int, text: str) -> str:
    """Return a Markdown ATX heading of the given level (1..6)."""
    if level < 1 or level > 6:
        raise ValueError(f"level must be 1..6, got {level}")
    return f"{'#' * level} {text}"


def table(headers: Sequence[str], rows: Sequence[Sequence[object]]) -> str:
    """Return a Markdown table (header + separator + rows) with deterministic ordering.

    Every cell is stringified verbatim; callers are responsible for
    pre-formatting numeric values so output is deterministic (Article 7).
    """
    header = "| " + " | ".join(headers) + " |"
    separator = "| " + " | ".join("---" for _ in headers) + " |"
    lines = [header, separator]
    for row in rows:
        lines.append("| " + " | ".join(str(cell) for cell in row) + " |")
    return "\n".join(lines)
