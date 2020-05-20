# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2020
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-04-15 09:26'
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


# 指定neq_key, 禁止两个参数相等
neq_key_params = {
    "p1": Rule(type=int),
    "p2": Rule(type=int, neq_key="p1")
}


@app.route("/neq/key", methods=["GET", "POST"])
@pre.catch(neq_key_params)
def neq_key_handler(params):
    return json_resp(params)


class TestNotEqualKey:

    def test_neq_key_smoke(self):
        """ 测试 neq_key 冒烟测试
        """
        resp = app.test_client().get("/neq/key", data={
            "p1": 15,
            "p2": 16
        })

        assert resp.json == {"p1": 15, "p2": 16}

    def test_neq_key_594(self):
        """ 测试 eq_key 异常
        """
        resp = app.test_client().get("/neq/key", data={
            "p1": 15,
            "p2": 15
        })

        assert resp.json["respCode"] == 594
