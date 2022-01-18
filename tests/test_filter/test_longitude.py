# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2020
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-04-13 14:36'


class TestLongitude:

    def test_longitude_smoke(self, client):
        """ 测试地理纬度
        """
        resp = client.get("/longitude", data={
            "p1": "116.3860159600"
        })

        assert resp.json == {"p1": "116.3860159600"}

    def test_longitude_590(self, client):
        """ 测试地理纬度 590 错误
        """
        resp = client.get("/longitude", data={
            "p1": "180.3860159600"
        })

        assert resp.json["respCode"] == 491
