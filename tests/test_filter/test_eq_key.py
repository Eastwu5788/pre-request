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


# 指定eq_key, 邀请
eq_key_params = {
    "p1": Rule(type=int, dest="P1"),
    "p2": Rule(type=int, eq_key="P1", dest="P2")
}


@app.route("/eq/key", methods=["GET", "POST"])
@pre.catch(eq_key_params)
def eq_key_handler(params):
    return json_resp(params)


class TestEqualKey:

    def test_eq_key_smoke(self):
        """ 测试 eq_key 冒烟测试
        """
        resp = app.test_client().get("/eq/key", data={
            "p1": 15,
            "p2": 15
        })

        assert resp.json == {"P1": 15, "P2": 15}

    def test_eq_key_593(self):
        """ 测试 eq_key 异常
        """
        resp = app.test_client().get("/eq/key", data={
            "p1": 15,
            "p2": 16
        })

        assert resp.json["respCode"] == 593
