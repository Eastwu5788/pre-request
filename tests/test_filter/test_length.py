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

    def test_length_filter_574(self, client):
        """ 测试 length_filter 574 错误
        """

        resp = client.get("/length", data={
            "params": "h",
            "params2": "aaa"
        })
        assert resp.json["respCode"] == 474

    def test_length_filter_575(self, client):
        """ 测试 length_filter 575 错误
        """

        resp = client.get("/length", data={
            "params": "he",
            "params2": "aa"
        })
        assert resp.json["respCode"] == 475

    def test_length_filter_576(self, client):
        """ 测试 length_filter 576 错误
        """

        resp = client.get("/length", data={
            "params": "hello",
            "params2": "aaa"
        })
        assert resp.json["respCode"] == 476

    def test_length_filter_577(self, client):
        """ 测试 length_filter 577 错误
        """

        resp = client.get("/length", data={
            "params": "he",
            "params2": "jerry"
        })
        assert resp.json["respCode"] == 477
