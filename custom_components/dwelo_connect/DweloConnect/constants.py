from enum import Enum

DWELO_SWITCH_TYPE = "switch"
DWELO_THERMOSTAT_TYPE = "Thermostat"
DWELO_LOCK_TYPE = "lock"

#THERMOSTAT COMMANDS
class ClimateControl(Enum):
    COOL = "cool"
    OFF = "off"
    HEAT = "heat"

#SWITCH COMMANDS
class SwitchControl(Enum):
    ON = "on"
    OFF = "off"

#LOCK COMMANDS
class LockControl(Enum):
    LOCK = "lock"
    UNLOCK = "unlock"



