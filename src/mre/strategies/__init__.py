"""Strategy plugins (ARC-005 §6, ARC-008 ARC-ACT-010)."""

from mre.strategies.exp001 import EXP001_STRATEGY_ID, exp001_signal_definition  # noqa: F401
from mre.strategies.exp005 import PRICE_BREAKOUT_STRATEGY_ID, exp005_signal_definition  # noqa: F401
from mre.strategies.exp007 import SWING_BREAKOUT_STRATEGY_ID, exp007_signal_definition  # noqa: F401
from mre.strategies.registry import StrategyDefinition, get, register, registered_ids  # noqa: F401
