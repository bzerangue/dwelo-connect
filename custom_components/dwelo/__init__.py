"""Support for Dwelo Service."""
import logging

import voluptuous as vol

from homeassistant.const import CONF_DEVICES, CONF_PASSWORD, CONF_TIMEOUT, CONF_USERNAME
from homeassistant.helpers import discovery
import homeassistant.helpers.config_validation as cv
from importlib import import_module

# DweloConnect = import_module(".DweloConnect")
from .DweloConnect.dwelo import DweloAccount
from .DweloConnect.dwelo_thermostat import DweloThermostat
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

    # temp = list(filter(lambda d: isinstance(d, DweloThermostat), dwelo_devices))[0]
    # switches = list(filter(lambda d: isinstance(d, DweloSwitch), dwelo_devices))
    # hass.data[DWELO_DEVICES].append(temp)
    # hass.data[DWELO_DEVICES].append(switches)
    # _LOGGER.info(hass.data[DWELO_DEVICES])
    # if CONF_DEVICES in config[DOMAIN] and config[DOMAIN].get(CONF_DEVICES):
    #     configured_devices = config[DOMAIN].get(CONF_DEVICES)
    #     for device in configured_devices:
    #         dyson_device = next(
    #             (d for d in dyson_devices if d.serial == device["device_id"]), None
    #         )
    #         if dyson_device:
    #             try:
    #                 connected = dyson_device.connect(device["device_ip"])
    #                 if connected:
    #                     _LOGGER.info("Connected to device %s", dyson_device)
    #                     hass.data[DYSON_DEVICES].append(dyson_device)
    #                 else:
    #                     _LOGGER.warning("Unable to connect to device %s", dyson_device)
    #             except OSError as ose:
    #                 _LOGGER.error(
    #                     "Unable to connect to device %s: %s",
    #                     str(dyson_device.network_device),
    #                     str(ose),
    #                 )
    #         else:
    #             _LOGGER.warning(
    #                 "Unable to find device %s in Dyson account", device["device_id"]
    #             )
    # else:
    #     # Not yet reliable
    #     for device in dyson_devices:
    #         _LOGGER.info(
    #             "Trying to connect to device %s with timeout=%i and retry=%i",
    #             device,
    #             timeout,
    #             retry,
    #         )
    #         connected = device.auto_connect(timeout, retry)
    #         if connected:
    #             _LOGGER.info("Connected to device %s", device)
    #             hass.data[DYSON_DEVICES].append(device)
    #         else:
    #             _LOGGER.warning("Unable to connect to device %s", device)

    # # Start fan/sensors components
    if hass.data[DWELO_DEVICES]:
        _LOGGER.debug("Starting sensor/fan components")
        for platform in DWELO_PLATFORMS:
            discovery.load_platform(hass, platform, DOMAIN, {}, config)

    return True
