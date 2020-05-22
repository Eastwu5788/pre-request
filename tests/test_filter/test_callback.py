# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2020
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-03-18 13:25'
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


def call_back_func(value):
    if value == "3":
        return 999
    return value


callback_params = {
    "params": Rule(type=str, callback=call_back_func)
}


@app.route("/callback", methods=['get', 'post'])
@pre.catch(callback_params)
def callback_handler(params):
    """ 测试自定义处理callback校验
    """
    return json_resp(params)


class TestCallBack:

    def test_call_back_smoke(self):
        """ 测试回调函数
        """
        resp = app.test_client().get("/callback", data={
            "params": 3
        })

        assert resp.json == {"params": 999}

        resp = app.test_client().get("/callback", data={
            "params": "3"
        })

        assert resp.json == {"params": 999}

        resp = app.test_client().get("/callback", data={
            "params": 5
        })

        assert resp.json == {"params": "5"}
