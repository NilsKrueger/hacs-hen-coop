"""Sensor platform for HenCoop."""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.components.sensor import SensorEntity, SensorEntityDescription

from .const import LOGGER
from .entity import HenCoopEntity

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from .coordinator import HenCoopDataUpdateCoordinator
    from .data import HenCoopConfigEntry

ENTITY_DESCRIPTIONS = (
    SensorEntityDescription(
        key="top",
        name="Hen Coop Door Top Sensor",
        icon="mdi:door",
    ),
    SensorEntityDescription(
        key="bottom",
        name="Hen Coop Door Bottom Sensor",
        icon="mdi:door",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001 Unused function argument: `hass`
    entry: HenCoopConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    async_add_entities(
        HenCoopDoorSensor(
            coordinator=entry.runtime_data.coordinator,
            entity_description=entity_description,
        )
        for entity_description in ENTITY_DESCRIPTIONS
    )


class HenCoopDoorSensor(HenCoopEntity, SensorEntity):
    """Hen Coop Door Sensor class."""

    def __init__(
        self,
        coordinator: HenCoopDataUpdateCoordinator,
        entity_description: SensorEntityDescription,
    ) -> None:
        """Initialize the sensor class."""
        # Pass the entity_description key as unique_id_suffix to the parent class
        super().__init__(coordinator, unique_id_suffix=entity_description.key)
        self.entity_description = entity_description
        # Use proper type for _attr_name (str or None)
        self.entity_description = entity_description
        LOGGER.debug(f"Sensor initialized with unique_id: {self._attr_unique_id}")

    @property
    def native_value(self) -> bool | None:
        """Return the native value of the sensor."""
        return self.coordinator.data.get(self.entity_description.key)
