"""
Custom integration to integrate HenCoop with Home Assistant.

For more details about this integration, please refer to
https://github.com/NilsKrueger/integration_bluephacs-hen-cooprint
"""

from __future__ import annotations

from datetime import timedelta
from typing import TYPE_CHECKING

from homeassistant.const import CONF_API_TOKEN, CONF_HOST, Platform
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.loader import async_get_loaded_integration

from .api import HenCoopApiClient
from .const import DOMAIN, LOGGER
from .coordinator import HenCoopDataUpdateCoordinator
from .data import HenCoopData

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant

    from .data import HenCoopConfigEntry

PLATFORMS: list[Platform] = [
    # Platform.SENSOR,
    Platform.BINARY_SENSOR,
    Platform.COVER,
    # Platform.SWITCH,
]


# https://developers.home-assistant.io/docs/config_entries_index/#setting-up-an-entry
async def async_setup_entry(
    hass: HomeAssistant,
    entry: HenCoopConfigEntry,
) -> bool:
    """Set up this integration using UI."""
    coordinator = HenCoopDataUpdateCoordinator(
        hass=hass,
        logger=LOGGER,
        name=DOMAIN,
        update_interval=timedelta(hours=1),
    )
    entry.runtime_data = HenCoopData(
        client=HenCoopApiClient(
            host=entry.data[CONF_HOST],
            token=entry.data[CONF_API_TOKEN],
            session=async_get_clientsession(hass),
        ),
        integration=async_get_loaded_integration(hass, entry.domain),
        coordinator=coordinator,
    )

    # https://developers.home-assistant.io/docs/integration_fetching_data#coordinated-single-api-poll-for-data-for-all-entities
    await coordinator.async_config_entry_first_refresh()

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    entry.async_on_unload(entry.add_update_listener(async_reload_entry))

    return True


async def async_unload_entry(
    hass: HomeAssistant,
    entry: HenCoopConfigEntry,
) -> bool:
    """Handle removal of an entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)


async def async_reload_entry(
    hass: HomeAssistant,
    entry: HenCoopConfigEntry,
) -> None:
    """Reload config entry."""
    await hass.config_entries.async_reload(entry.entry_id)
