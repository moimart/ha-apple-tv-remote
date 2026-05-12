"""Config flow for the Apple TV Remote integration."""

from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.selector import (
    EntitySelector,
    EntitySelectorConfig,
)

from .const import CONF_NAME, CONF_REMOTE, DOMAIN


def _apple_tv_remote_entities(hass: Any) -> list[str]:
    """Return entity_ids of `remote.*` entities created by `apple_tv`."""
    registry = er.async_get(hass)
    return [
        entry.entity_id
        for entry in registry.entities.values()
        if entry.domain == "remote" and entry.platform == "apple_tv"
    ]


class AppleTvRemoteConfigFlow(ConfigFlow, domain=DOMAIN):
    """Walk the user through picking which Apple TV and naming the bundle."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Initial step: pick the Apple TV remote entity and name the bundle."""
        candidates = _apple_tv_remote_entities(self.hass)
        if not candidates:
            return self.async_abort(reason="no_apple_tvs")

        errors: dict[str, str] = {}

        if user_input is not None:
            remote: str = user_input[CONF_REMOTE]
            name: str = user_input[CONF_NAME].strip()
            if not name:
                errors[CONF_NAME] = "name_required"
            elif remote not in candidates:
                errors[CONF_REMOTE] = "remote_unavailable"
            else:
                await self.async_set_unique_id(f"{remote}::{name.lower()}")
                self._abort_if_unique_id_configured()
                return self.async_create_entry(
                    title=name,
                    data={CONF_REMOTE: remote, CONF_NAME: name},
                )

        schema = vol.Schema(
            {
                vol.Required(CONF_NAME): str,
                vol.Required(CONF_REMOTE): EntitySelector(
                    EntitySelectorConfig(include_entities=candidates)
                ),
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=schema,
            errors=errors,
        )
