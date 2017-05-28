# -*- coding: utf-8 -*-
"""The utilities module. Include packages/modules here to be used by the Assisant"""

import requests
import os

class DB():
    def __init__(self):
        self.base_url="https://jsonbin.org/me"
        self.DB_KEY=os.environ["DB_KEY"]

    def get(self,key):
        url=self.base_url+"/"+key
        headers={"authorization":"token {}".format(self.DB_KEY)}
        r=requests.get(url, headers=headers)
        if r.status_code!=200 or r.text=='null':
            return None
        return r.text

    def put(self,key,value):
        url=self.base_url
        payload={key:value}
        headers={"authorization":"token {}".format(self.DB_KEY)}
        r=requests.patch(url, headers=headers,data=payload)
        if r.status_code!=201:
            return -1
        return r.text

    def delete(self,key):
        url=self.base_url+"/"+key
        headers={"authorization":"token {}".format(self.DB_KEY)}
        r=requests.delete(url, headers=headers)
        if r.status_code!=200:
            return -1
        return 0
