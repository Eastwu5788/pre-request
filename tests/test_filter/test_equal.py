# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2020
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-03-27 15:51'


class TestEqual:

    def test_equal_filter_smoke(self, client):
        """ 测试 equal_filter 过滤器
        """
        resp = client.get("/equal", data={
            "p1": 1,
            "p2": "1",
            "p3": 2,
            "p4": "aaa"
        })

        assert resp.json == {"p1": 1, "p2": "1", "p3": 2, "p4": "aaa"}

    def test_equal_filter_578(self, client):
        """ 测试 equal_filter 过滤器
        """
        resp = client.get("/equal", data={
            "p1": 2,
            "p2": "1",
            "p3": 2,
            "p4": "aaa"
        })

        assert resp.json["respCode"] == 578

        resp = client.get("/equal", data={
            "p1": 1,
            "p2": "2",
            "p3": 2,
            "p4": "aaa"
        })

        assert resp.json["respCode"] == 578

    def test_equal_filter_579(self, client):
        """ 测试 equal_filter 过滤器
        """
        resp = client.get("/equal", data={
            "p1": 1,
            "p2": "1",
            "p3": 1,
            "p4": "aaa"
        })

        assert resp.json["respCode"] == 579

        resp = client.get("/equal", data={
            "p1": 1,
            "p2": "1",
            "p3": 2,
            "p4": "1"
        })

        assert resp.json["respCode"] == 579
