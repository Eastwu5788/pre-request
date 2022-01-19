# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2020
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-04-13 14:17'


class TestIpv4:

    def test_ipv4_smoke(self, client):
        """ 测试IPV4地址验证
        """
        resp = client.get("/ipv4", data={
            "p1": "127.0.0.1"
        })

        assert resp.json == {"p1": "127.0.0.1"}

    def test_ipv4_587(self, client):
        """ 测试ipv4 587 异常
        """
        resp = client.get("/ipv4", data={
            "p1": "127.0.0.256"
        })

        assert resp.json["respMsg"] == "p1 field does not conform to ipv4 format"
