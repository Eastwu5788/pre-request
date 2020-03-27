# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2020
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-03-18 13:25'


class TestCallBack:

    def test_call_back_smoke(self, client):
        """ 测试回调函数
        """
        resp = client.get("/callback", data={
            "params": 3
        })

        assert resp.json == {"params": 999}

        resp = client.get("/callback", data={
            "params": "3"
        })

        assert resp.json == {"params": 999}

        resp = client.get("/callback", data={
            "params": 5
        })

        assert resp.json == {"params": "5"}
