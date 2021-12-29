"""Support for August lock."""
import logging

# from august.activity import ActivityType
# from august.lock import LockStatus
# from august.util import update_lock_detail_from_activity

from .DweloConnect.dwelo_lock import (
    DweloLock,
    LockControl,
)

from homeassistant.components.lock import ATTR_CHANGED_BY, LockDevice
from homeassistant.const import ATTR_BATTERY_LEVEL
from homeassistant.core import callback
from homeassistant.helpers.restore_state import RestoreEntity

from . import DWELO_DEVICES

_LOGGER = logging.getLogger(__name__)


def setup_platform(hass, config, add_devices, discovery_info=None):
    """Set up the Dwelo Lock."""
    if discovery_info is None:
        return
    # Get Dyson Devices from parent component.
    add_devices(
        [
            DweloLockDevice(device)
            for device in hass.data[DWELO_DEVICES]
            if isinstance(device, DweloLock)
        ]
    )


class DweloLockDevice(LockDevice):
    """Representation of an Dwelo lock."""

    def __init__(self, device: DweloLock):
        """Initialize the switch."""
        self._device = device
        self._device_id = device.deviceid

    def lock(self, **kwargs):
        """Lock the device."""
        self._device.Lock()

    def unlock(self, **kwargs):
        """Unlock the device."""
        self._device.Unlock()

    @property
    def should_poll(self):
        """No polling needed."""
        return True

    @property
    def name(self):
        """Return the name of this device."""
        return self._device.name

    # @property
    # def available(self):
    #     """Return the availability of this sensor."""
    #     return self._available

    @property
    def is_locked(self):
        """Return true if device is on."""
        if self._device.GetLockStatus() is LockControl.LOCK:
            return True
        return False

    # @property
    # def changed_by(self):
    #     """Last change triggered by."""
    #     return self._changed_by

    @property
    def device_state_attributes(self):
        """Return the device specific state attributes."""
        attributes = {ATTR_BATTERY_LEVEL: self._device.GetLockBattery()}
        return attributes

    # async def async_added_to_hass(self):
    #     """Restore ATTR_CHANGED_BY on startup since it is likely no longer in the activity log."""
    #     await super().async_added_to_hass()

    #     last_state = await self.async_get_last_state()
    #     if not last_state:
    #         return

    #     if ATTR_CHANGED_BY in last_state.attributes:
    #         self._changed_by = last_state.attributes[ATTR_CHANGED_BY]

    @property
    def unique_id(self) -> str:
        """Get the unique id of the lock."""
        return str(self._device.deviceid)

    def update(self):
        self._device.GetState(True)
