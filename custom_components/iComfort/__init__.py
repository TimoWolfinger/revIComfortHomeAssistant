from homeassistant import core
from .gateway import IComfortGateway
from homeassistant.helpers import device_registry as dr
from .const import DOMAIN
async def async_setup(hass: core.HomeAssistant, config: dict) -> bool:
    """Set up the REV Ritter IComfort component."""
    # @TODO: Add setup code.
    
    gateway = IComfortGateway(hass, config)
    if not await gateway.async_initialize_gateway(): 
        return False
    
    # add Gateway to device registry
    device_registry = dr.async_get(hass)
    gw_info = gateway.api.getInfo()
    unique_id = gw_info.u
    gateway = device_registry.async_get_or_create(
        config_entry_id=config.entry_id,
        connections={(dr.CONNECTION_NETWORK_MAC, unique_id)},
        identifiers={(DOMAIN, unique_id)},
        manufacturer="REV_Ritter",
        name=gw_info.w,
        model=gw_info.w,
        sw_version=gw_info.v,
        
    )
    hass.helpers.discovery.load_platform('switch', DOMAIN, {}, config)
  
    return True
