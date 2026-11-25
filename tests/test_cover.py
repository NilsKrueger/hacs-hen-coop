"""Run with python -m unittest discover -s tests in the HA dev environment."""

# ruff: noqa: S101 -- assertions are intentional in tests
import unittest
from importlib import import_module
from unittest.mock import MagicMock

cover = import_module("custom_components.hacs-hen-coop.cover")


class CoverTests(unittest.TestCase):
    """Verify how controller status is presented in HA."""

    def test_stopped_between_contacts(self) -> None:
        """A timeout does not imply an end position."""
        coordinator = MagicMock()
        coordinator.data = {
            "top": False,
            "bottom": False,
            "motion": "idle",
            "last_stop_reason": "timeout",
        }
        entity = cover.HenCoopDoorCover(coordinator, cover.ENTITY_DESCRIPTIONS[0])
        assert entity.is_closed is None
        assert not entity.is_closing
        assert entity.extra_state_attributes["last_stop_reason"] == "timeout"
        del coordinator.data["last_stop_reason"]  # Older Pi firmware
        assert entity.extra_state_attributes["last_stop_reason"] is None
