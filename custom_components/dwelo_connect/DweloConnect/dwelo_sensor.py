from enum import Enum

class DweloSensor(Enum):
    TEMPERATURE = "temperature"
    HUMIDITY = "humidity"
    LIGHT = "light"
    BATTERY = "battery"
    LOCK = "lock"
    COOL_TEMP = "setToCool"
    HEAT_TEMP = "setToHeat"
    SETPOINT = "setpoint"
    CLIMATE_MODE = "mode"
