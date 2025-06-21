"""Adds config flow for HenCoop."""

from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_API_TOKEN, CONF_HOST
from homeassistant.helpers import selector
from homeassistant.helpers.aiohttp_client import async_create_clientsession

from .api import (
    HenCoopApiClient,
    HenCoopApiClientAuthenticationError,
    HenCoopApiClientCommunicationError,
    HenCoopApiClientError,
)
from .const import DOMAIN, LOGGER


class HenCoopFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for HenCoop."""

    VERSION = 1

    async def async_step_user(
        self,
        user_input: dict | None = None,
    ) -> config_entries.ConfigFlowResult:
        """Handle a flow initialized by the user."""
        _errors = {}
        if user_input is not None:
            try:
                await self._test_credentials(
                    host=user_input[CONF_HOST],
                    token=user_input[CONF_API_TOKEN],
                )
            except HenCoopApiClientAuthenticationError as exception:
                LOGGER.warning(exception)
                _errors["base"] = "auth"
            except HenCoopApiClientCommunicationError as exception:
                LOGGER.error(exception)
                _errors["base"] = "connection"
            except HenCoopApiClientError as exception:
                LOGGER.exception(exception)
                _errors["base"] = "unknown"
            else:
                return self.async_create_entry(
                    title="HenCoop",
                    data=user_input,
                )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_HOST): selector.TextSelector(
                        selector.TextSelectorConfig(
                            type=selector.TextSelectorType.URL,
                        ),
                    ),
                    vol.Required(CONF_API_TOKEN): selector.TextSelector(
                        selector.TextSelectorConfig(
                            type=selector.TextSelectorType.PASSWORD,
                        ),
                    ),
                },
            ),
            errors=_errors,
        )

    async def _test_credentials(self, host: str, token: str) -> None:
        """Validate credentials."""
        client = HenCoopApiClient(
            host=host,
            token=token,
            session=async_create_clientsession(self.hass),
        )
        await client.async_door_status()
