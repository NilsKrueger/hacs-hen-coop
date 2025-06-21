"""Binary sensor platform for hacs-hen-coop."""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
    BinarySensorEntityDescription,
)

from .const import LOGGER
from .entity import HenCoopEntity

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from .coordinator import HenCoopDataUpdateCoordinator
    from .data import HenCoopConfigEntry

ENTITY_DESCRIPTIONS = (
    BinarySensorEntityDescription(
        key="top",
        name="HenCoop Binary Sensor Top",
        device_class=BinarySensorDeviceClass.CONNECTIVITY,
    ),
    BinarySensorEntityDescription(
        key="bottom",
        name="HenCoop Binary Sensor Bottom",
        device_class=BinarySensorDeviceClass.CONNECTIVITY,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001 Unused function argument: `hass`
    entry: HenCoopConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the binary_sensor platform."""
    LOGGER.debug(f"Setting up HenCoop binary sensors from entry {entry.entry_id}")

    async_add_entities(
        HenCoopBinarySensor(
            coordinator=entry.runtime_data.coordinator,
            entity_description=entity_description,
        )
        for entity_description in ENTITY_DESCRIPTIONS
    )


class HenCoopBinarySensor(HenCoopEntity, BinarySensorEntity):
    """HenCoop binary_sensor class."""

    def __init__(
        self,
        coordinator: HenCoopDataUpdateCoordinator,
        entity_description: BinarySensorEntityDescription,
    ) -> None:
        """Initialize the binary_sensor class."""
        # Pass the entity_description key as unique_id_suffix to the parent class
        super().__init__(coordinator, unique_id_suffix=entity_description.key)
        self.entity_description = entity_description
        # Use proper type for _attr_name (str or None)
        self.entity_description = entity_description
        LOGGER.debug(
            f"Binary sensor initialized with unique_id: {self._attr_unique_id}"
        )

    @property
    def is_on(self) -> bool | None:
        """Return true if the binary_sensor is on."""
        return self.coordinator.data.get(self.entity_description.key)
