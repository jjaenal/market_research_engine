"""Order domain model (ARC-002 §7.7)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Order:
    """An entry or exit instruction at simulation level (FND-009 §14.1).

    Live execution is out of scope (PRD-001 §11).
    """

    order_type: str
    side: str
    price: float
    trigger: Any
    execution_status: str
