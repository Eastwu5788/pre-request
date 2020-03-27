# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2020
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-03-18 09:56'


class TestEmpty:

    def test_empty_smoke(self, client):
        """ 验证 empty_filter 插件
        """
        resp = client.get("/empty", data={
            "int": 1,
            "str": "ds",
            "int2": 4,
            "str2": "5"
        })

        assert resp.json == {'int': '1', 'int2': '4', 'str': 'ds', 'str2': '5'}

        resp = client.get("/empty", data={
            "int": 0,
            "str": 2,
        })
        assert resp.json == {'int': '0', 'int2': 1, 'str': '2', 'str2': None}

    def test_empty_560(self, client):
        """ 验证 empty_filter 560 错误
        """
        resp = client.get("/empty", data={
            "int3": 1,
            "str": "ds",
            "int2": 4,
            "str2": "5"
        })
        assert resp.json["respCode"] == 560

        # int 传值为None
        resp = client.get("/empty", data={
            "int": None,
            "str": "ds",
        })
        assert resp.json["respCode"] == 560

        # int 传值为0，str传值为None
        resp = client.get("/empty", data={
            "int": 0,
            "str": None,
        })
        assert resp.json["respCode"] == 560
