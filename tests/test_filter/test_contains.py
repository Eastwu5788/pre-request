# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2020
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-04-13 13:28'


class TestContains:

    def test_contains_smoke(self, client):
        """ 测试字符串包含函数
        """
        resp = client.get("/contains", data={
            "p1": "abcdef"
        })

        assert resp.json == {"p1": "abcdef"}

    def test_contains_581(self, client):
        """ 测试字符串包含 581 异常
        """
        resp = client.get("/contains", data={
            "p1": "abdef"
        })

        assert resp.json["respMsg"] == "'p1' need required content"
