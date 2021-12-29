"""Dwelo Connect package."""

from .apiclient import ApiClient
import json

from .dwelo_switch import DweloSwitch
from .dwelo_lock import DweloLock
from .dwelo_thermostat import DweloThermostat

from .util import is_lock, is_switch, is_thermostat


class DweloAccount(object):
    def __init__(self, username, password):
        self.username = username
        self.password = password

        self._client = ApiClient()
        self.token = None
        self.uid = None
        self.cid = None
        self.gid = None

        self.device_json = None
        self.devices = []

    def login(self):
        user = {
            "email": self.username,
            "password": self.password,
            "applicationId": "concierge",
        }
        token_json = self._client.doPost("v3/login", json.dumps(user), None, None)
        if token_json is not None:
            ApiClient.token = token_json["token"]
            self.token = token_json["token"]
            self.uid = token_json["user"]["uid"]
            return True
        return False

    def get_devices(self):
        return self.device_setup()

    def device_setup(self):
        self.get_community()
        self.get_gateway()
        self.get_devices_api()
        self.get_device_state()

        for device in self.device_json:
            dyson_device = None
            if is_switch(device):
                dyson_device = DweloSwitch(device)
            if is_lock(device):
                dyson_device = DweloLock(device)
            if is_thermostat(device):
                dyson_device = DweloThermostat(device)

            if dyson_device is not None:
                self.devices.append(dyson_device)
        return self.devices

    def get_community(self):
        param = {"limit": 5000, "offset": 0}
        community_json = self._client.doGet("v3/community/", None, param)
        self.cid = community_json["results"][0]["uid"]

    def get_gateway(self):
        param = {"communityId": self.cid}
        gateway_json = self._client.doGet("v4/address/", None, param)
        self.gid = gateway_json["results"][0]["gatewayId"]

    def get_devices_api(self):
        param = {"gatewayId": self.gid, "limit": 5000, "offset": 0}
        devices_json = self._client.doGet("v3/device/", None, param)
        self.device_json = devices_json["results"]

    def get_device_state(self):
        state_json = self._client.doGet(f"v3/sensor/gateway/{self.gid}/")
        for i, val in enumerate(self.device_json):
            val["state"] = list(
                filter(lambda x: x["deviceId"] == val["uid"], state_json["results"])
            )
