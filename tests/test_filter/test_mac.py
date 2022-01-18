# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2020
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-04-13 14:25'


class TestMac:

    def test_mac_smoke(self, client):
        """ 测试mac地址验证
        """
        resp = client.get("/mac", data={
            "p1": "34:29:8f:98:16:e4"
        })

        assert resp.json == {"p1": "34:29:8f:98:16:e4"}

    def test_ipv4_589(self, client):
        """ 测试mac 589 异常
        """
        resp = client.get("/mac", data={
            "p1": "34:29:8f:98:16:eg"
        })

        assert resp.json["respCode"] == 489
