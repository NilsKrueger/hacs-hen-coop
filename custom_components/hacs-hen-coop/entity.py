"""HenCoopEntity class."""

from __future__ import annotations

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import ATTRIBUTION, DOMAIN, LOGGER
from .coordinator import HenCoopDataUpdateCoordinator


class HenCoopEntity(CoordinatorEntity[HenCoopDataUpdateCoordinator]):
    """HenCoopEntity class."""

    _attr_attribution = ATTRIBUTION

    def __init__(
        self,
        coordinator: HenCoopDataUpdateCoordinator,
        unique_id_suffix: str | None = None,
    ) -> None:
        """Initialize."""
        super().__init__(coordinator)
        # Allow overriding the unique_id with a suffix
        if unique_id_suffix:
            self._attr_unique_id = (
                f"{coordinator.config_entry.entry_id}_{unique_id_suffix}"
            )
            LOGGER.debug(f"Created entity with unique_id: {self._attr_unique_id}")
        else:
            self._attr_unique_id = coordinator.config_entry.entry_id

        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, coordinator.config_entry.entry_id)},
            name="Hen Coop Controller",
            manufacturer="HACS",
        )
