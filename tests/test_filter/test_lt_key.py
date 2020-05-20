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


# 指定lt_key, 限定一个参数必须小于另一个参数
lt_key_params = {
    "p1": Rule(type=int, dest="P1"),
    "p2": Rule(type=int, lt_key="P1")
}


@app.route("/lt/key", methods=["GET", "POST"])
@pre.catch(lt_key_params)
def lt_key_handler(params):
    return json_resp(params)


class TestLtKey:

    def test_lt_key_smoke(self):
        """ 测试 lt_key 冒烟测试
        """
        resp = app.test_client().get("/lt/key", data={
            "p1": 15,
            "p2": 13
        })

        assert resp.json == {"P1": 15, "p2": 13}

    def test_lt_key_596(self):
        """ 测试 gt_key 异常
        """
        resp = app.test_client().get("/lt/key", data={
            "p1": 15,
            "p2": 15
        })

        assert resp.json["respCode"] == 597

        resp = app.test_client().get("/lt/key", data={
            "p1": 15,
            "p2": 16
        })

        assert resp.json["respCode"] == 597
