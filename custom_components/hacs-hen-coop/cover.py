"""Cover platform for HenCoop."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from homeassistant.components.cover import (
    CoverDeviceClass,
    CoverEntity,
    CoverEntityDescription,
    CoverEntityFeature,
)

from .const import LOGGER
from .entity import HenCoopEntity

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from .coordinator import HenCoopDataUpdateCoordinator
    from .data import HenCoopConfigEntry

ENTITY_DESCRIPTIONS = (
    CoverEntityDescription(
        key="door",
        name="Hen Coop Door",
        icon="mdi:door-sliding",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001
    entry: HenCoopConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the cover platform."""
    LOGGER.debug(f"Setting up HenCoop cover from entry {entry.entry_id}")

    async_add_entities(
        HenCoopDoorCover(
            coordinator=entry.runtime_data.coordinator,
            entity_description=entity_description,
        )
        for entity_description in ENTITY_DESCRIPTIONS
    )


class HenCoopDoorCover(HenCoopEntity, CoverEntity):
    """Hen Coop Door Cover class."""

    def __init__(
        self,
        coordinator: HenCoopDataUpdateCoordinator,
        entity_description: CoverEntityDescription,
    ) -> None:
        """Initialize the cover class."""
        super().__init__(coordinator, unique_id_suffix=entity_description.key)
        self.entity_description = entity_description
        self._attr_device_class = CoverDeviceClass.SHUTTER
        self._attr_supported_features = (
            CoverEntityFeature.OPEN | CoverEntityFeature.CLOSE | CoverEntityFeature.STOP
        )
        LOGGER.debug(f"Cover initialized with unique_id: {self._attr_unique_id}")

    @property
    def is_closed(self) -> bool | None:
        """Return if the cover is closed."""
        if not self.coordinator.data:
            return None

        door_top = self.coordinator.data.get("top", False)
        door_bottom = self.coordinator.data.get("bottom", False)

        # Door is considered closed when bottom sensor is triggered
        return not door_top and door_bottom

    @property
    def is_opening(self) -> bool | None:
        """Return if the cover is opening."""
        # This would require tracking door movement state
        return None

    @property
    def is_closing(self) -> bool | None:
        """Return if the cover is closing."""
        # This would require tracking door movement state
        return None

    async def async_open_cover(self, **kwargs: Any) -> None:
        """Open the cover."""
        LOGGER.debug("Opening hen coop door")
        await self.coordinator.config_entry.runtime_data.client.async_open_door()
        await self.coordinator.async_request_refresh()

    async def async_close_cover(self, **kwargs: Any) -> None:
        """Close the cover."""
        LOGGER.debug("Closing hen coop door")
        await self.coordinator.config_entry.runtime_data.client.async_close_door()
        await self.coordinator.async_request_refresh()

    async def async_stop_cover(self, **kwargs) -> None:
        """Stop the cover."""
        LOGGER.debug("Stopping hen coop door")
        await self.coordinator.config_entry.runtime_data.client.async_stop()
        await self.coordinator.async_request_refresh()
