from .constants import DWELO_LOCK_TYPE, DWELO_SWITCH_TYPE, DWELO_THERMOSTAT_TYPE

def is_switch(json_payload):
    if json_payload['deviceType'].lower() == DWELO_SWITCH_TYPE.lower():
        return True
    return False

def is_lock(json_payload):
    if json_payload['deviceType'].lower() == DWELO_LOCK_TYPE.lower():
        return True
    return False

def is_thermostat(json_payload):
    if json_payload['deviceType'].lower() == DWELO_THERMOSTAT_TYPE.lower():
        return True
    return False
        