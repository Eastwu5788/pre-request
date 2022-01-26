# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2020
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-04-15 09:27'
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


# 指定lte_key, 限定一个参数必须小于另一个参数
lte_key_params = {
    "p1": Rule(type=int),
    "p2": Rule(type=int, lte_key="p1")
}


@app.route("/lte/key", methods=["GET", "POST"])
@pre.catch(lte_key_params)
def lte_key_handler(params):
    return json_resp(params)


class TestGtKey:

    def test_gt_key_smoke(self):
        """ 测试 gt_key 冒烟测试
        """
        resp = app.test_client().get("/lte/key", data={
            "p1": 15,
            "p2": 13
        })

        assert resp.json == {"p1": 15, "p2": 13}

        resp = app.test_client().get("/lte/key", data={
            "p1": 15,
            "p2": 15
        })

        assert resp.json == {"p1": 15, "p2": 15}

    def test_gt_key_595(self):
        """ 测试 gt_key 异常
        """
        resp = app.test_client().get("/lte/key", data={
            "p1": 15,
            "p2": 16
        })

        assert resp.json["respMsg"] == "'p2' should be less than or equal to 'p1'"
