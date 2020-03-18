# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2020
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-03-18 10:42'


class TestLength:

    def test_length_filter_smoke(self, client):
        """ 测试 length_filter 过滤器
        """
        resp = client.get("/length", data={
            "params": "ta",
            "params2": "aaa"
        })

        assert resp.json == {"params": "ta", "params2": "aaa"}

    def test_length_filter_561(self, client):
        """ 测试 length_filter 561 错误
        """

        resp = client.get("/length", data={
            "params": "hello",
            "params2": "aaa"
        })
        assert resp.json["respCode"] == 561

        resp = client.get("/length", data={
            "params": "ta",
            "params2": "aaaa"
        })
        assert resp.json["respCode"] == 561
