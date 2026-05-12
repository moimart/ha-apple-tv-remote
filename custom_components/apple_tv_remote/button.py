"""Button entities — one per Apple TV remote command."""

from __future__ import annotations

import asyncio
import logging

from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .commands import BUTTONS, ButtonSpec
from .const import CONF_NAME, CONF_REMOTE, DOMAIN

_LOGGER = logging.getLogger(__name__)

SERVICE_CALL_TIMEOUT = 8.0
"""Seconds to wait for the underlying ``remote.send_command`` service.

When the target Apple TV is unreachable the service call can hang on
TCP retries inside pyatv. Bail out after this many seconds so the
button press fails fast rather than blocking on the dashboard side.
"""


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Spawn one button entity per command."""
    async_add_entities(AppleTvRemoteButton(entry, spec) for spec in BUTTONS)


class AppleTvRemoteButton(ButtonEntity):
    """One press = one IR-style command sent to the underlying Apple TV."""

    _attr_has_entity_name = True

    def __init__(self, entry: ConfigEntry, spec: ButtonSpec) -> None:
        """Initialise the button."""
        self._entry_id = entry.entry_id
        self._remote_entity_id: str = entry.data[CONF_REMOTE]
        self._spec = spec
        self._attr_name = spec.friendly_name
        self._attr_icon = spec.icon
        self._attr_unique_id = f"{entry.entry_id}_{spec.key}"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.entry_id)},
            "name": entry.data[CONF_NAME],
            "manufacturer": "Apple",
            "model": "Apple TV (remote bridge)",
        }

    async def async_press(self) -> None:
        """Forward the press to HA's `apple_tv` remote entity."""
        try:
            async with asyncio.timeout(SERVICE_CALL_TIMEOUT):
                await self.hass.services.async_call(
                    domain="remote",
                    service="send_command",
                    service_data={"command": self._spec.remote_command},
                    target={"entity_id": self._remote_entity_id},
                    blocking=True,
                )
        except TimeoutError as err:
            _LOGGER.warning(
                "remote.send_command(%s) on %s timed out after %ss",
                self._spec.remote_command,
                self._remote_entity_id,
                SERVICE_CALL_TIMEOUT,
            )
            raise HomeAssistantError(
                f"Apple TV {self._remote_entity_id} did not respond within "
                f"{SERVICE_CALL_TIMEOUT}s"
            ) from err
