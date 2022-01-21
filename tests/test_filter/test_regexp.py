# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2020
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-03-18 12:52'


class TestRegexp:

    def test_regexp_filter_smoke(self, client):
        """ 测试 regexp_filter 过滤器
        """
        resp = client.get("/regexp", data={
            "params": "2020-03-03"
        })

        assert resp.json == {"params": "2020-03-03"}

    def test_regexp_filter_566(self, client):
        """ 测试 regexp_filter 566 错误
        """
        resp = client.get("/regexp", data={
            "params": "2020-3-03"
        })

        assert resp.json["respMsg"] == "'params' does not match the regular expression"

        resp = client.get("/regexp", data={
            "params": "2020-03"
        })

        assert resp.json["respMsg"] == "'params' does not match the regular expression"
