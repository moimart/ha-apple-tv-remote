"""Button entities — one per Apple TV remote command."""

from __future__ import annotations

from typing import Any

from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .commands import BUTTONS, ButtonSpec
from .const import CONF_NAME, CONF_REMOTE, DOMAIN


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
        if self._spec.remote_command == "_power_toggle":
            await self._power_toggle()
            return
        await self.hass.services.async_call(
            domain="remote",
            service="send_command",
            service_data={"command": self._spec.remote_command},
            target={"entity_id": self._remote_entity_id},
            blocking=True,
        )

    async def _power_toggle(self) -> None:
        """Toggle Apple TV power via the pyatv-backed send_command path.

        HA's high-level ``remote.turn_on`` / ``remote.turn_off`` services
        for apple_tv don't reliably wake the device — the verified pattern
        is to route through ``remote.send_command`` with ``wakeup`` or
        ``turn_off`` as the literal command argument, which pyatv handles
        directly.
        """
        state = self.hass.states.get(self._remote_entity_id)
        is_on = state is not None and state.state == "on"
        command = "turn_off" if is_on else "wakeup"
        await self.hass.services.async_call(
            domain="remote",
            service="send_command",
            service_data={"command": command},
            target={"entity_id": self._remote_entity_id},
            blocking=True,
        )
