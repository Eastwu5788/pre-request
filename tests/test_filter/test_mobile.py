# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2020
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-03-18 10:58'


class TestMobile:

    def test_mobile_filter_smoke(self, client):
        """ 测试 mobile_filter 冒烟测试
        """
        resp = client.get("/mobile", data={
            "params": "13899998888"
        })

        assert resp.json == {"params": "13899998888"}

    def test_mobile_filter_565(self, client):
        """ 测试 mobile_filter 565 错误
        """
        resp = client.get("/mobile", data={
            "params": "138999988880"
        })
        assert resp.json["respCode"] == 565

        resp = client.get("/mobile", data={
            "params": "138999988a8"
        })
        assert resp.json["respCode"] == 565

        resp = client.get("/mobile", data={
            "params": "1389999888"
        })
        assert resp.json["respCode"] == 565
