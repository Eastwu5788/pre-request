# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2020
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-04-13 14:18'


class TestIpv6:

    def test_ipv6_smoke(self, client):
        """ 测试IPV6地址验证
        """
        resp = client.get("/ipv6", data={
            "p1": "CDCD:910A:2222:5498:8475:1111:3900:2020"
        })

        assert resp.json == {"p1": "CDCD:910A:2222:5498:8475:1111:3900:2020"}

    def test_ipv6_588(self, client):
        """ 测试ipv4 588 异常
        """
        resp = client.get("/ipv6", data={
            "p1": "1030::C9B4:FF12:48AA:1A2BA"
        })

        assert resp.json["respMsg"] == "p1 field does not conform to ipv6 format"
