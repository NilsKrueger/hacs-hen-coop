"""DataUpdateCoordinator for hacs-hen-coop."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import (
    HenCoopApiClientAuthenticationError,
    HenCoopApiClientError,
)
from .const import LOGGER

if TYPE_CHECKING:
    from .data import HenCoopConfigEntry


# https://developers.home-assistant.io/docs/integration_fetching_data#coordinated-single-api-poll-for-data-for-all-entities
class HenCoopDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the API."""

    config_entry: HenCoopConfigEntry

    async def _async_update_data(self) -> Any:
        """Update data via library."""
        try:
            data = await self.config_entry.runtime_data.client.async_door_status()
            LOGGER.debug(f"API response: {data}")
            return data  # noqa: TRY300
        except HenCoopApiClientAuthenticationError as exception:
            raise ConfigEntryAuthFailed(exception) from exception
        except HenCoopApiClientError as exception:
            raise UpdateFailed(exception) from exception
