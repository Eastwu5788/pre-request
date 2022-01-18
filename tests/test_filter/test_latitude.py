# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2020
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-04-13 14:36'


class TestLatitude:

    def test_latitude_smoke(self, client):
        """ 测试地理纬度
        """
        resp = client.get("/latitude", data={
            "p1": "39.9077465200"
        })

        assert resp.json == {"p1": "39.9077465200"}

    def test_latitude_590(self, client):
        """ 测试地理纬度 590 错误
        """
        resp = client.get("/latitude", data={
            "p1": "239.9077465200"
        })

        assert resp.json["respCode"] == 490
