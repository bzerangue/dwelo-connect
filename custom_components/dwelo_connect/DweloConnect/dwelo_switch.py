from .dwelo_device import DweloDevice
from .constants import SwitchControl
from .apiclient import ApiClient
from .dwelo_sensor import  DweloSensor
import json

class DweloSwitch(DweloDevice):
    def SetMode(self, mode):
        command = {
            "command": mode.value
        }
        self._client.doPost(f"v3/device/{self.deviceid}/command/",json.dumps(command),None, None)
    
    def GetSwitchStatus(self):
        lightstate = list(filter(lambda x: x['sensorType'] == DweloSensor.LIGHT.value, self.state))[0]
        if lightstate['value'] == SwitchControl.OFF.value:
            self.lightstate = SwitchControl.OFF
        else:
            self.lightstate = SwitchControl.ON
        return self.lightstate