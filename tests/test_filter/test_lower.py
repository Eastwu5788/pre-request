# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2020
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-04-13 13:56'


class TestLower:

    def test_lower_smoke(self, client):
        """ 测试字符串指定前缀
        """
        resp = client.get("/lower", data={
            "p1": "TEST"
        })

        assert resp.json == {"p1": "test"}
