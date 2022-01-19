# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2020
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-04-13 13:48'


class TestStartswith:

    def test_startswith_smoke(self, client):
        """ 测试字符串指定前缀
        """
        resp = client.get("/startswith", data={
            "p1": "abcTest"
        })

        assert resp.json == {"p1": "abcTest"}

    def test_contains_584(self, client):
        """ 测试字符串指定前缀 584 异常
        """
        resp = client.get("/startswith", data={
            "p1": "aoe"
        })

        assert resp.json["respMsg"] == "p1 field must start with 'abc'"
