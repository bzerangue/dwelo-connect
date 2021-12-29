from .dwelo_device import DweloDevice
from .constants import ClimateControl
from .dwelo_sensor import DweloSensor
from .apiclient import ApiClient
import json


class DweloThermostat(DweloDevice):
    def SetMode(self, mode):
        command = {"command": mode.value}
        self._client.doPost(
            f"v3/device/{self.deviceid}/command/", json.dumps(command), None, None
        )

    def SetTemp(self, mode, temp):
        command = {"command": mode.value, "commandValue": temp}
        self._client.doPost(
            f"v3/device/{self.deviceid}/command/", json.dumps(command), None, None
        )

    def GetSensorTemperature(self):
        sensorTemp: float = list(
            filter(
                lambda x: x["sensorType"] == DweloSensor.TEMPERATURE.value, self.state
            )
        )[0]["value"]
        return float(sensorTemp)

    def GetSensorHumidity(self):
        sensorHumidity: float = list(
            filter(lambda x: x["sensorType"] == DweloSensor.HUMIDITY.value, self.state)
        )[0]["value"]
        return sensorHumidity

    def GetMode(self):
        sensorMode = list(
            filter(
                lambda x: x["sensorType"] == DweloSensor.CLIMATE_MODE.value, self.state
            )
        )[0]["value"]
        return ClimateControl(sensorMode)

    def GetSetPoint(self):
        setPoint: float = list(
            filter(lambda x: x["sensorType"] == DweloSensor.SETPOINT.value, self.state)
        )[0]["value"]
        return setPoint

    def GetSetPointCool(self):
        setPoint: float = list(
            filter(lambda x: x["sensorType"] == DweloSensor.COOL_TEMP.value, self.state)
        )[0]["value"]
        return setPoint

    def GetSetPointHeat(self):
        setPoint: float = list(
            filter(lambda x: x["sensorType"] == DweloSensor.HEAT_TEMP.value, self.state)
        )[0]["value"]
        return setPoint
