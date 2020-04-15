# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2020
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-04-15 09:26'


class TestEqualKey:

    def test_eq_key_smoke(self, client):
        """ 测试 eq_key 冒烟测试
        """
        resp = client.get("/eq/key", data={
            "p1": 15,
            "p2": 15
        })

        assert resp.json == {"p1": 15, "p2": 15}

    def test_eq_key_593(self, client):
        """ 测试 eq_key 异常
        """
        resp = client.get("/eq/key", data={
            "p1": 15,
            "p2": 16
        })

        assert resp.json["respCode"] == 593
