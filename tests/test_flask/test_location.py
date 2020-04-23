# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2020
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-04-23 15:52'


class TestLocation:

    def test_location_filter(self, client):
        """ 测试指定Location位置的数据
        """
        client.set_cookie("localhost", "p5", "5")
        resp = client.get("/location?p1=1", data={
            "p2": 2,
            "p3": 3,
        }, headers={
            "p4": "4",
            "p7": "7"
        })
        assert resp.json == {"p1": 1, "p2": 2, "p3": 3, "p4": 4, "p5": 5, "p7": 7}

        resp = client.get("/location/json", json={
            "p6": 6
        })
        assert resp.json == {"p6": 6}
