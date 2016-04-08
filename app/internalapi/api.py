#-*- coding: utf-8 -*-

from requests.auth import HTTPBasicAuth
import requests
import json

class GlobalApi():
    def __init__(self):
        pass

    def post(self, endpoint, dictionary):
        url = "http://127.0.0.1:7777/api/{0}".format(endpoint)
        header = {'Content-type': 'application/json'}
        req = requests.post(url, data=json.dumps(dictionary), auth=('thecallbacks', 'ag5346hs3gf142g32h4h4'), headers=header).json()
        print req
        return req

    def put(self, endpoint, case, dictionary):
        url = "http://127.0.0.1:7777/api/{0}/{1}".format(endpoint,case)
        header = {'Content-type': 'application/json'}
        req = requests.put(url, data=json.dumps(dictionary), auth=('thecallbacks', 'ag5346hs3gf142g32h4h4'), headers=header).json()
        print req
        return req

    def get(self, endpoint, case):
        url = "http://127.0.0.1:7777/api/{0}/{1}".format(endpoint, case)
        header = {'Content-type': 'application/json'}
        filters = [dict(name="status", op="eq", val='New')]
        params = dict(q=json.dumps(dict(filters=filters)))
        raw = requests.get(url, auth=('thecallbacks', 'ag5346hs3gf142g32h4h4'), params=params, headers=header).json()

        return raw

    def get_all(self, endpoint):
        url = "http://127.0.0.1:7777/api/{0}".format(endpoint)
        header = {'Content-type': 'application/json'}
        filters = [dict(name="status", op="eq", val="pending")]
        params = dict(q=json.dumps(dict(filters=filters)))
        payload = {'status': 'new'}
        raw = requests.get(url, auth=('thecallbacks', 'ag5346hs3gf142g32h4h4'), params=params, headers=header)
        #for t in raw:
        #    if t in endpoint:
        #        print raw[t][0]
        #        foo = json.dumps(raw[t][0])
        #        return foo
        return raw.json()
