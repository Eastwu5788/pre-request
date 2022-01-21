# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2020
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-03-18 10:09'


class TestEnum:

    def test_enum_filter_smoke(self, client):
        """ 测试 enum_filter 过滤器
        """
        resp = client.get("/enum", data={
            "params": 1,
            "params2": "a"
        })
        assert resp.json == {"params": 1, "params2": "a"}

    def test_enum_filter_563(self, client):
        """ 测试 enum_filter 563 错误
        """
        resp = client.get("/enum", data={
            "params": 9,
            "params2": "a"
        })
        assert resp.json["respMsg"] == "'params' must be one of the following '[1, 2, 3]'"

        resp = client.get("/enum", data={
            "params": 1,
            "params2": "e"
        })
        assert resp.json["respMsg"] == "'params2' must be one of the following '['a', 'b', 'c']'"
