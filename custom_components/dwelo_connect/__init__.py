"""Support for Dwelo Service."""
import logging

import voluptuous as vol

from homeassistant.const import CONF_DEVICES, CONF_PASSWORD, CONF_TIMEOUT, CONF_USERNAME
from homeassistant.helpers import discovery
import homeassistant.helpers.config_validation as cv
from importlib import import_module

# DweloConnect = import_module(".DweloConnect")
from .DweloConnect.dwelo import DweloAccount
from .DweloConnect.dwelo_device import DweloDevice
from .DweloConnect.dwelo_sensor import DweloSensor
from .DweloConnect.dwelo_thermostat import DweloThermostat
from .DweloConnect.dwelo_lock import DweloLock
from .DweloConnect.dwelo_switch import DweloSwitch


_LOGGER = logging.getLogger(__name__)

CONF_LANGUAGE = "language"
CONF_RETRY = "retry"

DEFAULT_NAME = "Dwelo"
DEFAULT_TIMEOUT = 5
DEFAULT_RETRY = 10
DWELO_DEVICES = "dwelo_devices"
DWELO_PLATFORMS = ["climate", "switch", "lock"]

DOMAIN = "dwelo"

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {
                vol.Required(CONF_USERNAME): cv.string,
                vol.Required(CONF_PASSWORD): cv.string,
            }
        )
    },
    extra=vol.ALLOW_EXTRA,
)


def setup(hass, config):
    """Set up the Dwelo parent component."""
    _LOGGER.info("Creating new Dwelo component")

    if DWELO_DEVICES not in hass.data:
        hass.data[DWELO_DEVICES] = []

    dwelo_client = DweloAccount(
        config[DOMAIN].get(CONF_USERNAME), config[DOMAIN].get(CONF_PASSWORD)
    )

    logged = dwelo_client.login()

    if not logged:
        _LOGGER.error("Not connected to Dwelo account. Unable to add devices")
        return False

    _LOGGER.info("Connected to Dwelo account")

    dwelo_devices = dwelo_client.get_devices()

    for d in dwelo_devices:
        hass.data[DWELO_DEVICES].append(d)

    # # Start fan/sensors components
    if hass.data[DWELO_DEVICES]:
        _LOGGER.debug("Starting sensor/fan components")
        for platform in DWELO_PLATFORMS:
            discovery.load_platform(hass, platform, DOMAIN, {}, config)

    return True
