"""Custom types for hacs-hen-coop."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.loader import Integration

    from .api import HenCoopApiClient
    from .coordinator import HenCoopDataUpdateCoordinator


type HenCoopConfigEntry = ConfigEntry[HenCoopData]


@dataclass
class HenCoopData:
    """Data for the HenCoop integration."""

    client: HenCoopApiClient
    coordinator: HenCoopDataUpdateCoordinator
    integration: Integration
