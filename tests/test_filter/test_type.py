# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2020
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-03-18 12:52'
# sys
import json
from datetime import (
    date,
    datetime
)
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
    "str": Rule(type=str),
    "dt1": Rule(type=datetime, fmt="%Y-%m-%d %H:%M"),
    "dt2": Rule(type=date, fmt="%Y-%m-%d")
}


@app.route("/type", methods=['get', 'post'])
@pre.catch(type_params)
def type_handler(params):
    """ 测试字段目标数据类型校验
    """
    if params["dt1"] == datetime(2021, 12, 13, 12, 30):
        params["dt1"] = "success"

    if params["dt2"] == date(2021, 11, 13):
        params["dt2"] = "success"

    return json_resp(params)


class TestType:

    def test_type_filter_smoke(self):
        """ 测试 type_filter 冒烟测试
        """
        resp = app.test_client().get("/type", data={
            "int": "3",
            "str": 2,
            "dt1": "2021-12-13 12:30",
            "dt2": "2021-11-13"
        })

        assert resp.json == {"dt1": "success", "dt2": "success", "int": 3, "str": "2"}

    def test_type_datetime_v1(self):
        resp = app.test_client().get("/type", data={
            "int": "3",
            "str": 2,
            "dt1": "2021-12-13 12:30:00",
            "dt2": "2021-11-13"
        })

        assert resp.json["respMsg"] == "'dt1' convert to date failed"

    def test_type_datetime_v2(self):
        resp = app.test_client().get("/type", data={
            "int": "3",
            "str": 2,
            "dt1": "2021-12-13 12:30",
            "dt2": "2021-11"
        })

        assert resp.json["respMsg"] == "'dt2' convert to date failed"
