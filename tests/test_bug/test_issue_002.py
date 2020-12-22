# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2020
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-10-12 15:55'
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


# 指定gte_key, 禁止两个参数相等
gte_key_params = {
    "p1": Rule(type=int, required=False, default=None),
    "p2": Rule(type=int, required=False, default=None, gte_key="p1", dest="P2")
}


@app.route("/gte/key", methods=["GET", "POST"])
@pre.catch(gte_key_params)
def gte_key_handler(params):
    return json_resp(params)


class TestGteKey:

    def test_gte_key_smoke(self):
        """ 测试 gte_key 冒烟测试
        """
        resp = app.test_client().get("/gte/key", data={
            "p2": 16
        })
        assert resp.json == {"p1": None, "P2": 16}

        resp = app.test_client().get("/gte/key", data={
        })
        assert resp.json == {"p1": None, "P2": None}

        resp = app.test_client().get("/gte/key", data={
            "p1": 14,
            "p2": 16
        })
        assert resp.json == {"p1": 14, "P2": 16}

    def test_gte_key_596(self):
        """ 测试 gte_key 异常
        """
        resp = app.test_client().get("/gte/key", data={
            "p1": 15,
            "p2": 14
        })

        assert resp.json["respCode"] == 596
