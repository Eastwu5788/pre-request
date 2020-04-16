# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2020
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-04-13 11:05'


class TestSkip:

    def test_skip_filter_smoke(self, client):
        """ 测试 skip_filter 冒烟测试
        """
        resp = client.get("/skip", data={
            "v1": "Hello",
            "v2": 18,
        })

        assert resp.json == {"v1": "Hello", "v2": 18.0}

    def test_trim_filter_v1(self, client):
        """ 测试 skip 过滤器异常
        """
        resp = client.get("/skip", data={
            "v1": None,
            "v2": None,
        })

        assert resp.json == {"v1": None, "v2": 30.0}
