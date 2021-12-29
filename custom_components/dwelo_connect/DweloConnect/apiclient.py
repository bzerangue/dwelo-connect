"""Dwelo Connect package."""

import http.client
import mimetypes
import ssl
import json
import requests
import logging
from requests_toolbelt.adapters.ssl import SSLAdapter
from urllib.parse import urljoin


_LOGGER = logging.getLogger(__name__)


class ApiClient(object):
    token = None

    def __init__(self):
        self.server = "https://api.dwelo.com"
        self.baseHeaders = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36"
        }
        self.baseUrl = self.server

        defaultSession = requests.Session()
        defaultSession.mount(self.server, SSLAdapter())
        defaultSession.headers = self.baseHeaders

        self.session = defaultSession

    def _makeRequest(self, method=None, url=None, data=None, headers=None, params=None):
        try:
            self.__addToken()

            response = self.session.request(
                method=method,
                url=urljoin(self.baseUrl, url),
                data=data,
                headers=headers,
                params=params,
            )

            try:
                json_body = json.loads(response.content)
            except ValueError as e:
                raise e

            return json_body
        except Exception as e:
            raise e

    def __addToken(self):
        if ApiClient.token is not None:
            self.session.headers["Authorization"] = f"Token {ApiClient.token}"

    def doPost(self, partialUrl, data, headers, params={}):
        headers = {"Content-Type": "application/json;charset=UTF-8"}
        return self._makeRequest(
            method="POST", url=partialUrl, data=data, headers=headers
        )

    def doGet(self, partialUrl, headers={}, params={}):
        return self._makeRequest(
            method="GET", url=partialUrl, headers=headers, params=params
        )
