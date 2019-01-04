# -*- coding: utf-8 -*-
# (C) Wu Dong, 2018
# All rights reserved
__author__ = 'Wu Dong <wudong@eastwu.cn>'
__time__ = '2018/9/6 11:16'
import pytest
import requests
import json

test_dict = {
    "lStocks": 0.2,
    "smStocks": 0.4,
    "hkStocks": 0.4,
    "convertBond": 0.6,
    "interestBond": 0.3,
    "creditBond": 0.2,
    "notStand": 0.1
}


class TestFlask(object):

    @pytest.mark.parametrize(
        'params, expected', (
                ({"age": 3, "name": "Hi", "email": "wudong@eastwu.cn"},
                 {'code': 563, 'message': 'age字段的取值只能是以下几种[1, 2]!'}),

        )
    )
    def test_get_request(self, params, expected):
        resp = requests.get("http://127.0.0.1:5000/test", params)
        assert resp.status_code == 200
        assert resp.json() == expected

    @pytest.mark.parametrize(
        'params, expected', (
                ({"age": 3, "name": "Hi", "email": "wudong@eastwu.cn"},
                 {'code': 563, 'message': 'age字段的取值只能是以下几种[1, 2]!'}),
        )
    )
    def test_post_request(self, params, expected):
        resp = requests.post("http://127.0.0.1:5000/test", params)
        assert resp.status_code == 200
        assert resp.json() == expected

    @pytest.mark.parametrize(
        'params, expected', (
                ({"year": "2018-01-11", "empty": "as", "call": "22"},
                 {'code': 200, 'message': 'age字段的取值只能是以下几种[1, 2]!'}),
        )
    )
    def test_post_request(self, params, expected):
        resp = requests.post("http://127.0.0.1:5000/post", params)
        assert resp.status_code == 200
        print(resp.json())
