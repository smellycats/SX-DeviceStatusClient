# -*- coding: utf-8 -*-
import json

import requests
from requests.auth import HTTPBasicAuth


class Ping(object):
    def __init__(self, **kwargs):
        self.host = kwargs['host']
        self.port = kwargs['port']

        self.headers = {'content-type': 'application/json'}

        self.status = False

    def get_ping(self, ip, timeout=15):
        """发送短信"""
        url = 'http://{0}:{1}/connect/ping/{2}'.format(
            self.host, self.port, ip)
        try:
            r = requests.get(url, timeout=timeout)
            if r.status_code == 200:
                return json.loads(r.text)
            else:
                self.status = False
                raise Exception(u'url: {url}, status: {code}, {text}'.format(
                    url=url, code=r.status_code, text=r.text))
        except Exception as e:
            self.status = False
            raise

