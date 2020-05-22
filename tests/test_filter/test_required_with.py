# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2020
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-04-13 11:21'
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


required_with_params = {
    "p1": Rule(required=False),
    "p2": Rule(required=False, required_with="p1", type=float)
}


@app.route("/required/with", methods=["GET", "POST"])
@pre.catch(required_with_params)
def required_with_handler(params):
    return json_resp(params)


class TestRequiredWith:

    def test_required_with_smoke(self):
        """ 测试 required_with 冒烟测试
        """
        resp = app.test_client().get("/required/with", data={
            "p1": "H",
            "p2": 13
        })

        assert resp.json == {"p1": "H", "p2": 13.0}

    def test_required_with_599(self):
        """ 测试 required_with 冒烟测试
        """
        resp = app.test_client().get("/required/with", data={
            "p1": "H",
            "p2": None
        })

        assert resp.json["respCode"] == 599

        resp = app.test_client().get("/required/with", data={
            "p1": None,
            "p2": None
        })

        assert resp.json == {"p1": None, "p2": None}
