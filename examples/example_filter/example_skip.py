# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2020
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-04-13 10:51'
""" 演示skip忽略请求参数功能，pre-request仅尝试将key和value添加到params参数字典中
"""

# sys
import json
# 3p
from flask import Flask, make_response
# project
from pre_request import pre, Rule


app = Flask(__name__)
app.config["TESTING"] = True


def json_resp(result):
    result = json.dumps(result)
    resp = make_response(result)
    resp.headers['Content-Type'] = 'application/json'
    return resp


skip_params = {
    "v1": Rule(skip=True, type=float, required=False, default=30.0),
    "v2": Rule(skip=False, type=float, required=False, default=30.0),
}


@app.route("/skip", methods=['get', 'post'])
@pre.catch(skip_params)
def skip_handler(params):
    """ 测试 skip 功能
    """
    return json_resp(params)


class TestSkip:

    def test_skip_filter_smoke(self):
        """ 测试 skip_filter 冒烟测试
        """
        resp = app.test_client().get("/skip", data={
            "v1": "Hello",
            "v2": 18,
        })

        assert resp.json == {"v1": "Hello", "v2": 18.0}

    def test_trim_filter_v1(self):
        """ 测试 skip 过滤器异常
        """
        resp = app.test_client().post("/skip", json={
            "v1": None,
            "v2": None,
        })

        assert resp.json == {"v1": None, "v2": 30.0}


if __name__ == "__main__":
    TestSkip().test_skip_filter_smoke()
