# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2020
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-03-18 10:21'
import json


class TestJson:

    def test_json_filter_smoke(self, client):
        """ 测试 json_filter 过滤器
        """
        resp = client.get("/json", data={
            "params": json.dumps({"hello": "world"})
        })

        assert resp.json == {"params": {"hello": "world"}}

    def test_json_filter_570(self, client):
        """ 测试 json_filter 570错误
        """
        resp = client.get("/json", data={
            "params": "T"
        })

        assert resp.json["respCode"] == 470

        resp = client.get("/json", data={
            "params": {"tt": "ss"}
        })

        assert resp.json["respCode"] == 470
