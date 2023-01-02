from homeassistant.config_entries import ConfigEntry
from  homeassistant.const import CONF_HOST
from homeassistant.exceptions import ConfigEntryNotReady
import async_timeout
import asyncio
import logging
from datetime import datetime
from .api import iComfortAPI
from .const import DOMAIN

__LOGGER = logging.getLogger(__name__)
class IComfortGateway:
    """ manage the Gateway """
    def __init__(self, hass, config_entry: ConfigEntry):
        """initialize the system. """
        self.config_entry = config_entry
        self.hass = hass
        self.api = iComfortAPI(config_entry[CONF_HOST])

    @property
    def host(self) -> str:
        """return the host of this Gateway"""
        return self.config_entry.data[CONF_HOST]
        
    async def async_initialize_gateway(self):
        """initialize connecttion with the api"""
        try:
            with async_timeout.timeout(10):
                await self.api.getInfo()
        except (
            asyncio.TimeoutError
        ) as err:
            raise ConfigEntryNotReady(f"Error connecting to the iComfort Gateway" + err)
        except Exception:
            __LOGGER.exception("Unknown error connecting to the IComfort Gateway")
            return False
        return True

    async def async_request_switch_on(self, switch_id):
        self.api.switch_on(switch_id)

    async def async_request_switch_off(self, switch_id):
        return self.api.switch_off(switch_id)

    async def async_get_device_status(self, switch_id):
        return self.api.get_device_status(switch_id)

    async def async_get_devices(self):
        self.api.getDevices()

    async def async_get_gateway_info(self):
        parsedInfo={}
        try:
            info = await self.api.getInfo()
            parsedInfo = {
                "Gateway-IP": info.n,
                "Gateway-Subnet-Mask": info.o,
                "Gatway-GW": info.p,
                "Gatway-DNS": info.q,
                "Gateway-Software-Ver": info.v,
                "Gateway-MAC": info.u,
                "Manufacturer": info.x,
                "Time": datetime.fromtimestamp(info.t)
            }
        except:
            __LOGGER.exception("Unknown error connecting to the IComfort Gateway")
        return parsedInfo