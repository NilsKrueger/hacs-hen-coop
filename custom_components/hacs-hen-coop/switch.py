"""Switch platform for HenCoop."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from homeassistant.components.switch import SwitchEntity, SwitchEntityDescription

from .const import LOGGER
from .entity import HenCoopEntity

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from .coordinator import HenCoopDataUpdateCoordinator
    from .data import HenCoopConfigEntry

ENTITY_DESCRIPTIONS = (
    SwitchEntityDescription(
        key="door",
        name="Switch Hen Coop Door",
        icon="mdi:door-open",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001
    entry: HenCoopConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the switch platform."""
    async_add_entities(
        HenCoopDoorSwitch(
            coordinator=entry.runtime_data.coordinator,
            entity_description=entity_description,
        )
        for entity_description in ENTITY_DESCRIPTIONS
    )


class HenCoopDoorSwitch(HenCoopEntity, SwitchEntity):
    """Hen Coop Door Switch class."""

    def __init__(
        self,
        coordinator: HenCoopDataUpdateCoordinator,
        entity_description: SwitchEntityDescription,
    ) -> None:
        """Initialize the switch class."""
        # Pass the entity_description key as unique_id_suffix to the parent class
        super().__init__(coordinator, unique_id_suffix=entity_description.key)
        self.entity_description = entity_description
        LOGGER.debug(f"Switch initialized with unique_id: {self._attr_unique_id}")

    @property
    async def is_on(self) -> bool:
        """Return true if the switch is on."""
        door_state = (
            await self.coordinator.config_entry.runtime_data.client.async_door_status()
        )
        door_top = door_state.get("top", False)
        door_bottom = door_state.get("bottom", False)

        # Door is considered "on" when top sensor is triggered but bottom isn't
        # This indicates the door is open
        return door_top and not door_bottom

    async def async_turn_on(self, **_: Any) -> None:
        """Turn on the switch."""
        await self.coordinator.config_entry.runtime_data.client.async_open_door()
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **_: Any) -> None:
        """Turn off the switch."""
        await self.coordinator.config_entry.runtime_data.client.async_close_door()
        await self.coordinator.async_request_refresh()
