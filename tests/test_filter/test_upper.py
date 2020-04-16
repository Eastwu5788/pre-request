# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2020
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-04-13 14:00'


class TestUpper:

    def test_upper_smoke(self, client):
        """ 测试字符串大写
        """
        resp = client.get("/upper", data={
            "p1": "test"
        })

        assert resp.json == {"p1": "TEST"}
