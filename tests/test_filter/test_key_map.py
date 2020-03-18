# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2020
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-03-18 13:25'


class TestKeyMap:

    def test_key_map_smoke(self, client):
        """ 测试 key_map 映射
        """
        resp = client.get("/keymap", data={
            "params": 222
        })

        assert resp.json == {"ttt": "222"}
