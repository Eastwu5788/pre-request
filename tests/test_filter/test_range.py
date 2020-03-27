# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2020
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-03-18 12:51'


class TestRange:

    def test_range_filter_smoke(self, client):
        """ 测试 range_filter 冒烟测试
        """
        resp = client.get("/range", data={
            "params": 11,
            "params2": 10
        })

        assert resp.json == {"params": 11, "params2": 10}

    def test_range_filter_568(self, client):
        """ 测试 range_filter 568 错误
        """
        resp = client.get("/range", data={
            "params": 9,
            "params2": 10,
        })

        assert resp.json["respCode"] == 568

    def test_range_filter_571(self, client):
        """ 测试 range_filter 571 错误
        """
        resp = client.get("/range", data={
            "params": 18,
            "params2": 9,
        })

        assert resp.json["respCode"] == 571

    def test_range_filter_572(self, client):
        """ 测试 range_filter 572 错误
        """
        resp = client.get("/range", data={
            "params": 22,
            "params2": 10,
        })

        assert resp.json["respCode"] == 572

    def test_range_filter_573(self, client):
        """ 测试 range_filter 573 错误
        """
        resp = client.get("/range", data={
            "params": 18,
            "params2": 18,
        })

        assert resp.json["respCode"] == 573
