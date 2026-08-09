"""Strategy plugins (ARC-005 §6, ARC-008 ARC-ACT-010)."""

from mre.strategies.exp001 import EXP001_STRATEGY_ID, exp001_signal_definition  # noqa: F401
from mre.strategies.registry import StrategyDefinition, get, register, registered_ids  # noqa: F401
