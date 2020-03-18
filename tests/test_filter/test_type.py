# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2020
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-03-18 12:52'


class TestType:

    def test_type_filter_smoke(self, client):
        """ 测试 type_filter 冒烟测试
        """
        resp = client.get("/type", data={
            "int": "3",
            "str": 2,
        })

        assert resp.json == {"int": 3, "str": "2"}
