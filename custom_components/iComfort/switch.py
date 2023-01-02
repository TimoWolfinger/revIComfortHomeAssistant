from homeassistant.components.switch import SwitchEntity
from homeassistant.const import CONF_HOST
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
from homeassistant.core import HomeAssistant
from custom_components import iComfort
from .gateway import IComfortGateway
from homeassistant.helpers.entity_platform import AddEntitiesCallback

def setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None
) -> None:
    gateway = IComfortGateway(hass, config)

    # add devices
    add_entities(MySwitch(gateway,entity) for entity in gateway.async_get_devices())



class MySwitch(SwitchEntity):
    _attr_has_entity_name = True
    _attr_icon="mdi:power-socket"

    @property
    def device_info(self):
        """Return the device info."""
        deviceInfo = self.gateway.async_get_gateway_info()
        
        return {
            "Gateway": deviceInfo,
            "ID": self.unique_id
        }
    
    async def update(self):
        return self.gateway.async_get_device_status(self.unique_id)

    def __init__(self, gateway: IComfortGateway, unique_id):
        self._is_on = False
        self.device_class = "outlet"
        self.gateway = gateway
        self.unique_id = unique_id
        
    async def async_turn_on(self, **kwargs):
        """Turn the entity on."""
        self.gateway.async_request_switch_on(self.unique_id)
        self._is_on = self.gateway.async_get_device_status(self.unique_id)

    async def async_turn_off(self, **kwargs):
        """Turn the entity off"""
        self.gateway.async_request_switch_off(self.unique_id)
        self._is_on = self.gateway.async_get_device_status(self.unique_id)
    
    async def async_toggle(self, **kwargs):
        if ( self._is_on ):
            self.async_turn_off
        else:
            self.async_turn_on