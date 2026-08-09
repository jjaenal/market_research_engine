"""Strategy plugin registry (ARC-005 §6, §10; ARC-008 ARC-ACT-010)."""

from __future__ import annotations

from mre.models.signal_rule import SignalRule

StrategyDefinition = tuple[SignalRule, ...]

_STRATEGIES: dict[str, StrategyDefinition] = {}


def register(strategy_id: str, definition: StrategyDefinition) -> None:
    """Register a strategy definition under a unique ``strategy_id`` (ARC-005 §10).

    The definition is the strategy's run output — a deterministic
    ``tuple[SignalRule, ...]`` that the Signal Engine consumes. The engine
    interface is unchanged; a plugin only supplies configuration.
    """
    if not strategy_id:
        raise ValueError("strategy_id must not be empty")
    if not definition:
        raise ValueError("definition must not be empty")
    if strategy_id in _STRATEGIES:
        raise ValueError(f"strategy already registered: {strategy_id}")
    _STRATEGIES[strategy_id] = definition


def get(strategy_id: str) -> StrategyDefinition:
    """Return the registered definition, or fail the experiment (PRD-003 §7.4)."""
    if strategy_id not in _STRATEGIES:
        raise ValueError(f"unknown strategy plugin: {strategy_id}")
    return _STRATEGIES[strategy_id]


def registered_ids() -> tuple[str, ...]:
    """Registered strategy ids in deterministic (sorted) order."""
    return tuple(sorted(_STRATEGIES))
