# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2020
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-05-06 09:30'
# sys
import json
from datetime import datetime

# 3p
from flask import make_response, Flask
from pre_request import pre, Rule


app = Flask(__name__)
app.config["TESTING"] = True
client = app.test_client()


def json_resp(result):
    result = json.dumps(result)
    resp = make_response(result)
    resp.headers['Content-Type'] = 'application/json'
    return resp


args = {
    "birthday": Rule(type=datetime),
    "happyDay": Rule(type=datetime, eq_key="birthday"),
    "publishDate": Rule(type=datetime, fmt="%Y-%m-%d", gte=datetime(2019, 11, 11), lte=datetime(2019, 12, 12))
}


@app.route("/datetime", methods=["GET", "POST"])
@pre.catch(args)
def datetime_handler(params):
    return json_resp({})


class TestDatetime:

    def test_datetime_smoke(self):
        """ 测试时间日期转换能力
        """
        resp = app.test_client().post("/datetime", data={
            "birthday": "2019-01-01 11:12:13",
            "publishDate": "2019-11-18",
            "happyDay": "2019-01-01 11:12:13"
        })

        assert resp.json == {}

    def test_datetime_593(self):
        resp = app.test_client().post("/datetime", data={
            "birthday": "2019-01-01 11:12:13",
            "publishDate": "2019-11-18",
            "happyDay": "2019-01-01 11:12:15"
        })

        assert resp.json["respMsg"] == "the value of 'happyDay' must be the same as the value of 'birthday'"

    def test_datetime_571(self):
        resp = app.test_client().post("/datetime", data={
            "birthday": "2019-01-01 11:12:13",
            "publishDate": "2019-11-10",
            "happyDay": "2019-01-01 11:12:13"
        })

        assert resp.json["respMsg"] == "publishDate field value must be greater than or equal to 2019-11-11 00:00:00"

    def test_datetime_573(self):
        resp = app.test_client().post("/datetime", data={
            "birthday": "2019-01-01 11:12:13",
            "publishDate": "2019-12-20",
            "happyDay": "2019-01-01 11:12:13"
        })

        assert resp.json["respMsg"] == "publishDate field value must be less than or equal to 2019-12-12 00:00:00"
