"""Hen Coop API Client."""

from __future__ import annotations

import socket
from typing import Any

import aiohttp
import async_timeout


class HenCoopApiClientError(Exception):
    """Exception to indicate a general API error."""


class HenCoopApiClientCommunicationError(
    HenCoopApiClientError,
):
    """Exception to indicate a communication error."""


class HenCoopApiClientAuthenticationError(
    HenCoopApiClientError,
):
    """Exception to indicate an authentication error."""


def _verify_response_or_raise(response: aiohttp.ClientResponse) -> None:
    """Verify that the response is valid."""
    if response.status in (401, 403):
        msg = "Invalid credentials"
        raise HenCoopApiClientAuthenticationError(
            msg,
        )
    response.raise_for_status()


class HenCoopApiClient:
    """Hen Coop API Client."""

    def __init__(
        self,
        host: str,
        token: str,
        session: aiohttp.ClientSession,
    ) -> None:
        """
        Initialize the API client.

        Args:
            host: The host address of the API server (including http:// and port)
            token: Bearer token for authentication
            session: aiohttp client session

        """
        self._host = host.rstrip("/")
        self._token = token
        self._session = session
        self._headers = {"Authorization": f"Bearer {token}"}

    async def async_read_gpio_pin(self, pin: int) -> dict[str, int]:
        """
        Read the logic level of a specific GPIO pin.

        Args:
            pin: GPIO pin number (1-40)

        Returns:
            Dict containing pin number and value

        """
        return await self._api_wrapper(
            method="get",
            url=f"{self._host}/gpio/{pin}",
        )

    async def async_open_door(
        self, duration: int = 120, duty_cycle: int = 75
    ) -> dict[str, Any]:
        """
        Open the coop door.

        Args:
            duration: Motor operation duration in seconds
            duty_cycle: PWM duty cycle percentage

        Returns:
            Status response

        """
        return await self._api_wrapper(
            method="post",
            url=f"{self._host}/open-door",
            params={"duration": duration, "duty_cycle": duty_cycle},
        )

    async def async_close_door(
        self, duration: int = 120, duty_cycle: int = 75
    ) -> dict[str, Any]:
        """
        Close the coop door.

        Args:
            duration: Motor operation duration in seconds
            duty_cycle: PWM duty cycle percentage

        Returns:
            Status response

        """
        return await self._api_wrapper(
            method="post",
            url=f"{self._host}/close-door",
            params={"duration": duration, "duty_cycle": duty_cycle},
        )

    async def async_stop(self) -> dict[str, Any]:
        """
        Stop all GPIO activity and clean up.

        Returns:
            Status response

        """
        return await self._api_wrapper(
            method="post",
            url=f"{self._host}/stop",
        )

    async def async_door_status(self) -> dict[str, Any]:
        """
        Get the current state of both reed sensors.

        Returns:
            Reed sensor states

        """
        return await self._api_wrapper(
            method="get",
            url=f"{self._host}/door-status",
        )

    async def _api_wrapper(
        self,
        method: str,
        url: str,
        data: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
    ) -> Any:
        """
        Make an API request.

        Args:
            method: HTTP method
            url: API endpoint URL
            data: Request body data
            params: Query parameters

        Returns:
            API response as JSON

        """
        try:
            async with async_timeout.timeout(10):
                response = await self._session.request(
                    method=method,
                    url=url,
                    headers=self._headers,
                    json=data,
                    params=params,
                )
                _verify_response_or_raise(response)
                return await response.json()

        except TimeoutError as exception:
            msg = f"Timeout error fetching information - {exception}"
            raise HenCoopApiClientCommunicationError(
                msg,
            ) from exception
        except (aiohttp.ClientError, socket.gaierror) as exception:
            msg = f"Error fetching information - {exception}"
            raise HenCoopApiClientCommunicationError(
                msg,
            ) from exception
        except Exception as exception:  # pylint: disable=broad-except
            msg = f"Something really wrong happened! - {exception}"
            raise HenCoopApiClientError(
                msg,
            ) from exception
