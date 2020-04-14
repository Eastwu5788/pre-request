# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2020
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-04-13 13:38'


class TestExcludes:

    def test_excludes_smoke(self, client):
        """ 测试字符串包含函数
        """
        resp = client.get("/excludes", data={
            "p1": "def"
        })

        assert resp.json == {"p1": "def"}

    def test_contains_581(self, client):
        """ 测试字符串包含 583 异常
        """
        resp = client.get("/excludes", data={
            "p1": "aoe"
        })

        assert resp.json["respCode"] == 583
