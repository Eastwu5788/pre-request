# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2020
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-03-18 12:52'


class TestTrim:

    def test_trim_filter_smoke(self, client):
        """ 测试 trim_filter 冒烟测试
        """
        resp = client.get("/trim", data={
            "params": " Test"
        })

        assert resp.json == {"params": "Test"}

        resp = client.get("/trim", data={
            "params": " Test "
        })

        assert resp.json == {"params": "Test"}
