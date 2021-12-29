from .apiclient import ApiClient
import logging
import json
import time

_LOGGER = logging.getLogger(__name__)


class DweloDevice(object):
    def __init__(self, json_body):
        self._deviceid = json_body["uid"]
        self._name = json_body["givenName"]
        self._devicetype = json_body["deviceType"]
        self._gatewayid = json_body["gatewayId"]
        self._online = json_body["isOnline"]
        self._state = json_body["state"]
        self._client = ApiClient()

    def GetState(self, afterSet: bool = False):
        if afterSet:
            time.sleep(5)
        states = self._client.doGet(f"v3/sensor/gateway/{self._gatewayid}/")["results"]
        filt = list(filter(lambda x: int(x["deviceId"]) == int(self._deviceid), states))
       # _LOGGER.info(json.dumps(filt, indent=4, sort_keys=True))
        self._state = filt

    @property
    def deviceid(self):
        return self._deviceid

    @property
    def name(self):
        return self._name

    @property
    def devicetype(self):
        return self._devicetype

    @property
    def gatewayid(self):
        return self._gatewayid

    @property
    def online(self):
        return self._online

    @property
    def state(self):
        return self._state
