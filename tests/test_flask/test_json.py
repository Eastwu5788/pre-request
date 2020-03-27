# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2020
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-03-18 13:17'


class TestJson:

    def test_json_filter(self, client):
        """ 测试POST提交参数
        """
        resp = client.post("/type", json={
            "int": "3",
            "str": 2,
        })

        assert resp.json == {"int": 3, "str": 2}
