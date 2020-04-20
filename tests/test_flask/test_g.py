# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2020
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-04-20 10:08'


class TestG:

    def test_g_smoke(self, client):
        """ 测试通过flask g获取请求参数
        """
        resp = client.get("/g", data={
            "email": "wudong@eastwu.cn"
        })

        assert resp.json == {"email": "wudong@eastwu.cn"}
