"""Support for Dwelo thermostat."""
import logging
import time

# from libpurecool.const import FocusMode, HeatMode, HeatState, HeatTarget
# from libpurecool.dyson_pure_hotcool_link import DysonPureHotCoolLink
# from libpurecool.dyson_pure_state import DysonPureHotCoolState

from .DweloConnect.dwelo_thermostat import (
    DweloThermostat,
    ClimateControl,
)

from homeassistant.components.climate import ClimateDevice
from homeassistant.components.climate.const import (
    CURRENT_HVAC_COOL,
    CURRENT_HVAC_HEAT,
    CURRENT_HVAC_OFF,
    HVAC_MODE_COOL,
    HVAC_MODE_HEAT,
    HVAC_MODE_OFF,
    SUPPORT_TARGET_TEMPERATURE,
)
from homeassistant.const import ATTR_TEMPERATURE, TEMP_FAHRENHEIT

from . import DWELO_DEVICES

_LOGGER = logging.getLogger(__name__)

SUPPORT_HVAG = [HVAC_MODE_COOL, HVAC_MODE_HEAT, HVAC_MODE_OFF]
SUPPORT_FLAGS = SUPPORT_TARGET_TEMPERATURE


def setup_platform(hass, config, add_devices, discovery_info=None):
    """Set up the Dwelo thermostat."""
    if discovery_info is None:
        return
    # Get Dyson Devices from parent component.
    add_devices(
        [
            DweloThermostatDevice(device)
            for device in hass.data[DWELO_DEVICES]
            if isinstance(device, DweloThermostat)
        ]
    )


class DweloThermostatDevice(ClimateDevice):
    """Representation of a Dwelo thermostat."""

    def __init__(self, device):
        """Initialize the thermostat."""
        self._device: DweloThermostat = device
        self._current_temp = None

    # async def async_added_to_hass(self):
    #     """Call when entity is added to hass."""
    #     self.hass.async_add_job(self._device.add_message_listener, self.on_message)

    # def on_message(self, message):
    #     """Call when new messages received from the climate."""
    #     if not isinstance(message, DysonPureHotCoolState):
    #         return

    #     _LOGGER.debug("Message received for climate device %s : %s", self.name, message)
    #     self.schedule_update_ha_state()

    @property
    def should_poll(self):
        """No polling needed."""
        return True

    @property
    def supported_features(self):
        """Return the list of supported features."""
        return SUPPORT_FLAGS

    @property
    def name(self):
        """Return the display name of this climate."""
        return self._device.name

    @property
    def temperature_unit(self):
        """Return the unit of measurement."""
        return TEMP_FAHRENHEIT

    @property
    def current_temperature(self):
        """Return the current temperature."""
        if self._device.GetSensorTemperature():
            self._current_temp: float = self._device.GetSensorTemperature()
        return float(self._current_temp)

    @property
    def target_temperature(self):
        """Return the target temperature."""
        target_temp = None
        if self.hvac_mode == HVAC_MODE_COOL:
            target_temp = self._device.GetSetPointCool()
        else:
            target_temp = self._device.GetSetPointHeat()
        return float(target_temp)

    #@property
    #def current_humidity(self):
    #    """Return the current humidity."""
    #    humidity = self._device.GetSensorHumidity()
     #   if humidity:
     #       if humidity == 0:
    #            return None
    #        return humidity
    #    return None

    @property
    def hvac_mode(self):
        """Return hvac operation ie. heat, cool mode.

        Need to be one of HVAC_MODE_*.
        """
        mode = self._device.GetMode()
        if mode == ClimateControl.COOL:
            return HVAC_MODE_COOL
        elif mode == ClimateControl.HEAT:
            return HVAC_MODE_HEAT
        else:
            return HVAC_MODE_OFF

    @property
    def hvac_modes(self):
        """Return the list of available hvac operation modes.

        Need to be a subset of HVAC_MODES.
        """
        return SUPPORT_HVAG

    @property
    def hvac_action(self):
        """Return the current running hvac operation if supported.

        Need to be one of CURRENT_HVAC_*.
        """
        mode = self._device.GetMode()
        if mode == ClimateControl.COOL:
            return CURRENT_HVAC_COOL
        elif mode == ClimateControl.HEAT:
            return CURRENT_HVAC_HEAT
        else:
            return CURRENT_HVAC_OFF

    def set_temperature(self, **kwargs):
        """Set new target temperature."""
        target_temp = kwargs.get(ATTR_TEMPERATURE)
        if target_temp is None:
            return
        target_temp = int(target_temp)
        _LOGGER.debug("Set %s temperature %s", self.name, target_temp)
        # Limit the target temperature into acceptable range.
        target_temp = min(self.max_temp, target_temp)
        target_temp = max(self.min_temp, target_temp)
        self._device.SetTemp(self._device.GetMode(), target_temp)
        self.schedule_update_ha_state(True)

    def set_hvac_mode(self, hvac_mode):
        """Set new target hvac mode."""
        _LOGGER.debug("Set %s heat mode %s", self.name, hvac_mode)
        if hvac_mode == HVAC_MODE_HEAT:
            self._device.SetMode(ClimateControl.HEAT)
        elif hvac_mode == HVAC_MODE_COOL:
            self._device.SetMode(ClimateControl.COOL)
        elif hvac_mode == HVAC_MODE_OFF:
            self._device.SetMode(ClimateControl.OFF)
        self.schedule_update_ha_state(True)

    @property
    def min_temp(self):
        """Return the minimum temperature."""
        return 60

    @property
    def max_temp(self):
        """Return the maximum temperature."""
        return 85

    def update(self):
        self._device.GetState(True)
