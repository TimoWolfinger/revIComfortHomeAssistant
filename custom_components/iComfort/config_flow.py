
import logging
from homeassistant.config_entries import (
    ConfigFlow,
)
from homeassistant.core import callback
from .const import (
    DOMAIN,
    DEFAULT_PORT,
    CONF_ICOMFORT_BRIDGE_IP
)
from homeassistant.const import CONF_DEVICE_CLASS, CONF_HOST, CONF_PORT
from homeassistant.helpers import config_validation as cv
from homeassistant.data_entry_flow import FlowResult

import os
import voluptuous as vol
from .api import iComfortAPI
_LOGGER = logging.getLogger(__name__)
RESULT_UNKNOWN = "unknown"

def _is_file(value: str) -> bool:
    """Validate that the value is an existing file."""
    file_in = os.path.expanduser(value)
    return os.path.isfile(file_in) and os.access(file_in, os.R_OK)

class iComfortFlowHandler(ConfigFlow, domain=DOMAIN):
    """ Handle the config flow"""

    VERSION = 1

    @callback
    def _show_setup_form(
        self,
        user_input: dict[str, Any] | None = None,
        error: str | None = None,
    ) -> FlowResult:
        """Show the setup form to the user."""
        host = user_input.get(CONF_ICOMFORT_BRIDGE_IP, "") if user_input else ""
        data_schema = vol.Schema(
            {
                vol.Required(CONF_HOST, default=host): str,
                vol.Required(CONF_PORT, default=DEFAULT_PORT): cv.port,
            },
        )
        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors={"base": error} if error else None,
        )
    
    async def _async_check_connection(
        self, user_input: dict[str, Any]
    ) -> tuple[str | None, str | None]:
        """Attempt to connect the iComfort Bridge."""

        try:
            api = iComfortAPI(user_input[CONF_HOST])
            res = api.getInfo()
            if (res.count == 0 ): raise ConnectionError("Could't connect to Gateway")
            unique_id = res.u
            return None, unique_id
        except:
            return RESULT_UNKNOWN

    async def async_step_user(self, user_input: dict[str, Any] | None = None) -> FlowResult:
        error = None

        if (user_input is not None):
            host = user_input[CONF_HOST]
            self._async_abort_entries_match({CONF_HOST: host})
            error, unique_id = self._async_check_connection(user_input)
            if (error is None):
                if (not unique_id):
                    return self.async_abort(reason="invalid_unique_id")
                await self.async_set_unique_id(unique_id)
                self._abort_if_unique_id_configured()

                return self.async_create_entry(
                    title = host,
                    data = user_input
                )
        return self._show_setup_form(user_input, error)
