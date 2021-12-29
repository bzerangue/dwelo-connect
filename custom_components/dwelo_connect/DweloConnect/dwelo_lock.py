from .dwelo_device import DweloDevice
from .constants import LockControl
from .dwelo_sensor import DweloSensor
from .apiclient import ApiClient
import json

class DweloLock(DweloDevice):
    def Lock(self):
        command = {
            "command": LockControl.LOCK.value
        }
        self._client.doPost(f"v3/device/{self.deviceid}/command/",json.dumps(command),None, None)

    def Unlock(self):
        command = {
            "command": LockControl.UNLOCK.value
        }
        self._client.doPost(f"v3/device/{self.deviceid}/command/",json.dumps(command),None, None)
    
    def GetLockStatus(self):
        lockState = list(filter(lambda x: x['sensorType'] == DweloSensor.LOCK.value, self.state))[0]
        if lockState['value'] == "unlocked":
            self.lockstatus = LockControl.UNLOCK
        else:
            self.lockstatus = LockControl.LOCK
        return self.lockstatus

    def GetLockBattery(self):
        lockbattery:float = list(filter(lambda x: x['sensorType'] == DweloSensor.BATTERY.value, self.state))[0]['value']
        return lockbattery