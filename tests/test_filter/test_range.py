# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2020
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-03-18 12:51'


class TestRange:

    def test_range_filter_smoke(self, client):
        """ 测试 range_filter 冒烟测试
        """
        resp = client.get("/range", data={
            "params": 11
        })

        assert resp.json == {"params": 11}

    def test_range_filter_567(self, client):
        """ 测试 range_filter 567 错误
        """
        resp = client.get("/range", data={
            "params": 22
        })

        assert resp.json["respCode"] == 567
