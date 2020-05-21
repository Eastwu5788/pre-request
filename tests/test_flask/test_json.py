# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2020
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-03-18 13:17'
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


type_params = {
    "int": Rule(type=int),
    "str": Rule(type=str)
}


@app.route("/type", methods=['get', 'post'])
@pre.catch(type_params)
def type_handler(params):
    """ 测试字段目标数据类型校验
    """
    return json_resp(params)


class TestJson:

    def test_json_filter(self):
        """ 测试POST提交参数
        """
        resp = app.test_client().post("/type", json={
            "int": "3",
            "str": 2,
        })

        assert resp.json == {"int": 3, "str": "2"}
