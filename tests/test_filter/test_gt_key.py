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


# 指定gt_key, 禁止两个参数相等
gt_key_params = {
    "p1": Rule(type=int),
    "p2": Rule(type=int, gt_key="p1", dest="P2")
}


@app.route("/gt/key", methods=["GET", "POST"])
@pre.catch(gt_key_params)
def gt_key_handler(params):
    return json_resp(params)


class TestGtKey:

    def test_gt_key_smoke(self):
        """ 测试 gt_key 冒烟测试
        """
        resp = app.test_client().get("/gt/key", data={
            "p1": 15,
            "p2": 16
        })

        assert resp.json == {"p1": 15, "P2": 16}

    def test_gt_key_595(self):
        """ 测试 gt_key 异常
        """
        resp = app.test_client().get("/gt/key", data={
            "p1": 15,
            "p2": 15
        })

        assert resp.json["respCode"] == 595
