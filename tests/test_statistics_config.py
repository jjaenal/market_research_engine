from __future__ import annotations

import dataclasses

import pytest

from mre.models.statistics import StatisticsConfig


def test_config_defaults() -> None:
    config = StatisticsConfig()
    assert config.min_sample == 30


def test_config_holds_fields() -> None:
    config = StatisticsConfig(min_sample=50)
    assert config.min_sample == 50


def test_config_is_frozen() -> None:
    config = StatisticsConfig()
    with pytest.raises(dataclasses.FrozenInstanceError):
        config.min_sample = 10


def test_config_validation() -> None:
    with pytest.raises(ValueError):
        StatisticsConfig(min_sample=0)
    with pytest.raises(ValueError):
        StatisticsConfig(min_sample=-1)
