# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2020
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-06-24 13:39'
# sys
import json
# 3p
from flask import Flask, make_response
# project
from pre_request import pre, Rule
from pre_request import missing

app = Flask(__name__)
app.config["TESTING"] = True


def json_resp(result):
    result = json.dumps(result)
    resp = make_response(result)
    resp.headers['Content-Type'] = 'application/json'
    return resp


skip_params = {
    "v1": Rule(type=float, required=False, default=30.0, dest="OV1"),
    "v2": Rule(type=float, required=True, default=30.0),
}


@app.route("/skip", methods=['get', 'post'])
@pre.catch(skip_params)
def skip_handler(params):
    """ 测试 skip 功能
    """
    if params["v2"] is missing:
        params["v2"] = None
    return json_resp(params)


class TestSkip:

    def test_skip_filter_smoke(self):
        """ 测试 skip_filter 冒烟测试
        """
        pre.skip_filter = True
        resp = app.test_client().get("/skip", data={
            "v1": "Hello",
        })
        pre.skip_filter = False
        assert resp.json == {"OV1": "Hello", "v2": None}
