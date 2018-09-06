# -*- coding: utf-8 -*-
# (C) Wu Dong, 2018
# All rights reserved
__author__ = 'Wu Dong <wudong@eastwu.cn>'
__time__ = '2018/9/6 11:07'
import requests
from tornado.escape import json_decode


def get_request():
    request_params = {"year": 1, "test": "word"}
    resp = requests.post("http://127.0.0.1:8000/test", request_params)

    # print(json_decode(resp.content))
    print(str(resp.content, encoding='utf-8'))


if __name__ == "__main__":
    get_request()
