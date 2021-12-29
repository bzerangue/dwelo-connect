"""Support for Dwelo switch."""
import logging
import time

# from pyHS100 import SmartDeviceException, SmartPlug
from .DweloConnect.dwelo_switch import (
    DweloSwitch,
    SwitchControl,
)

from homeassistant.components.switch import SwitchDevice
import homeassistant.helpers.device_registry as dr
from homeassistant.helpers.typing import HomeAssistantType

from . import DWELO_DEVICES

_LOGGER = logging.getLogger(__name__)


def setup_platform(hass, config, add_devices, discovery_info=None):
    """Set up the Dwelo Switch."""
    if discovery_info is None:
        return
    # Get Dyson Devices from parent component.
    add_devices(
        [
            DweloSwitchDevice(device)
            for device in hass.data[DWELO_DEVICES]
            if isinstance(device, DweloSwitch)
        ]
    )


# def add_entity(device: DweloSwitch, async_add_entities):
#     """Check if device is online and add the entity."""
#     # Attempt to get the sysinfo. If it fails, it will raise an
#     # exception that is caught by async_add_entities_retry which
#     # will try again later.
#     device.get_sysinfo()

#     async_add_entities([SmartPlugSwitch(device)], update_before_add=True)


# async def async_setup_entry(hass: HomeAssistantType, config_entry, async_add_entities):
#     """Set up switches."""
#     await async_add_entities_retry(
#         hass, async_add_entities, hass.data[TPLINK_DOMAIN][CONF_SWITCH], add_entity
#     )

#     return True


class DweloSwitchDevice(SwitchDevice):
    """Representation of a Dwelo switch."""

    # def __init__(self, device):
    # """Initialize the thermostat."""
    # self._device: DweloThermostat = device
    # self._current_temp = None

    def __init__(self, device: DweloSwitch):
        """Initialize the switch."""
        self._device = device
        self._sysinfo = None
        self._state = None
        self._available = False
        self._device_id = device.deviceid

    @property
    def unique_id(self):
        """Return a unique ID."""
        return self._device_id

    @property
    def name(self):
        """Return the name of the Switch."""
        return self._device.name

    # @property
    # def device_info(self):
    #     """Return information about the device."""
    #     return {
    #         "name": self._alias,
    #         "model": self._model,
    #         "manufacturer": "TP-Link",
    #         "connections": {(dr.CONNECTION_NETWORK_MAC, self._mac)},
    #         "sw_version": self._sysinfo["sw_ver"],
    #     }

    # @property
    # def available(self) -> bool:
    #     """Return if switch is available."""
    #     return self._available

    @property
    def should_poll(self):
        """No polling needed."""
        return True

    @property
    def is_on(self):
        """Return true if switch is on."""
        if self._device.GetSwitchStatus() is SwitchControl.ON:
            return True
        return False
        # return self._device.GetSwitchStatus()

    def turn_on(self, **kwargs):
        """Turn the switch on."""
        self._device.SetMode(SwitchControl.ON)
        self.schedule_update_ha_state(True)

    def turn_off(self, **kwargs):
        """Turn the switch off."""
        self._device.SetMode(SwitchControl.OFF)
        self.schedule_update_ha_state(True)

    # @property
    # def device_state_attributes(self):
    #     """Return the state attributes of the device."""
    #     return self._emeter_params

    # @property
    # def _plug_from_context(self):
    #     """Return the plug from the context."""
    #     children = self.smartplug.sys_info["children"]
    #     return next(c for c in children if c["id"] == self.smartplug.context)

    def update(self):
        """Update the TP-Link switch's state."""

        self._device.GetState(True)
