"""Config flow for EcoFlow STREAM."""

from __future__ import annotations

import voluptuous as vol

from homeassistant import config_entries

from .const import DOMAIN


class EcoFlowStreamConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for EcoFlow STREAM."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            return self.async_create_entry(
                title="EcoFlow STREAM",
                data=user_input,
            )

        schema = vol.Schema(
            {
                vol.Required("access_key"): str,
                vol.Required("secret_key"): str,
                vol.Required("device_sn"): str,
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=schema,
            errors=errors,
        )
