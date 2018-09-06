# -*- coding: utf-8 -*-
# (C) Wu Dong, 2018
# All rights reserved
__author__ = 'Wu Dong <wudong@eastwu.cn>'
__time__ = '2018/9/6 11:16'
import pytest
import requests


class TestTornado(object):

    @pytest.mark.parametrize(
        'params, expected', (
                ({"age": 1920, "name": "Hi", "email": "wudong@eastwu.cn"},
                 {'code': 560, 'message': 'mobile字段不能为空!'}),

        )
    )
    def test_get_request(self, params, expected):
        resp = requests.get("http://127.0.0.1:8000/test", params)
        assert resp.status_code == 200
        assert resp.json() == expected

    @pytest.mark.parametrize(
        'params, expected', (
                ({"year": 1, "test": "word"},
                 {'year': 1, 'test': 'word'}),
        )
    )
    def test_post_request(self, params, expected):
        resp = requests.post("http://127.0.0.1:8000/test", params)
        assert resp.status_code == 200
        assert str(resp.content, encoding='utf-8') == str(expected)

