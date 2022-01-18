# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2020
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-03-18 09:29'


class TestEmail:

    def test_email_filter_smoke(self, client):
        """ 测试Email过滤器 冒烟测试
        """
        resp = client.get("/email", data={
            "email": "wudong@eastwu.cn"
        })

        assert resp.status_code == 200
        assert resp.json == {"email": "wudong@eastwu.cn"}

    def test_email_filter_564(self, client):
        """ 测试Email过滤器 触发 564 错误
        """
        resp = client.get("/email", data={
            "email": "wudong@@eastwu.cn"
        })

        assert resp.status_code == 200
        assert resp.json["respCode"] == 464

    def test_email_filter_560(self, client):
        """ 测试Email过滤器 触发 错误
        """
        resp = client.get("/email", data={
            "em": "wudong@eastwu.cn"
        })

        assert resp.status_code == 200
        assert resp.json["respCode"] == 460
