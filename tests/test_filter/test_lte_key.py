# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2020
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-04-15 09:27'

class TestGtKey:

    def test_gt_key_smoke(self, client):
        """ 测试 gt_key 冒烟测试
        """
        resp = client.get("/gt/key", data={
            "p1": 15,
            "p2": 16
        })

        assert resp.json == {"p1": 15, "p2": 16}

    def test_gt_key_595(self, client):
        """ 测试 gt_key 异常
        """
        resp = client.get("/gt/key", data={
            "p1": 15,
            "p2": 15
        })

        assert resp.json["respCode"] == 595
