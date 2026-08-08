"""Signal domain model (ARC-002 §7.6)."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass(frozen=True)
class Signal:
    """A strategy output indicating a condition is met (FND-009 §13.1).

    Aggregates the constituent Events (Article 4) so the decision can
    always be explained (Article 5). Immutable per Article 13.
    """

    signal_type: str
    timestamp: datetime
    events: tuple[Any, ...]
    confirmation: bool = True
    source_strategy: str = ""
    experiment_id: str = ""
