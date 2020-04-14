# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2020
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-04-13 13:35'


class TestContainsAny:

    def test_contains_any_smoke(self, client):
        """ 测试字符串任意包含函数
        """
        resp = client.get("/contains/any", data={
            "p1": "aef"
        })

        assert resp.json == {"p1": "aef"}

    def test_contains_582(self, client):
        """ 测试字符串任意包含 582 异常
        """
        resp = client.get("/contains/any", data={
            "p1": "def"
        })

        assert resp.json["respCode"] == 582
