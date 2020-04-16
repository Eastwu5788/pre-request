# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2020
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-04-13 11:21'


class TestRequiredWith:

    def test_required_with_smoke(self, client):
        """ 测试 required_with 冒烟测试
        """
        resp = client.get("/required/with", data={
            "p1": "H",
            "p2": 13
        })

        assert resp.json == {"p1": "H", "p2": 13.0}

    def test_required_with_599(self, client):
        """ 测试 required_with 冒烟测试
        """
        resp = client.get("/required/with", data={
            "p1": "H",
            "p2": None
        })

        assert resp.json["respCode"] == 599

        resp = client.get("/required/with", data={
            "p1": None,
            "p2": None
        })

        assert resp.json == {"p1": None, "p2": None}
