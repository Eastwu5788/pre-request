# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2020
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-05-26 10:54'
import json
from flask import Flask, make_response
from pre_request import pre, Rule
from pre_request import ParamsValueError

app = Flask(__name__)
app.config["TESTING"] = True
client = app.test_client()


def json_resp(result):
    result = json.dumps(result)
    resp = make_response(result)
    resp.headers['Content-Type'] = 'application/json'
    return resp


email_params = {
    "params": Rule(reg=r'^[A-Za-z\d]+([-_.][A-Za-z\d]+)*@([A-Za-z\d]+[-.])+[A-Za-z\d]{2,4}$')
}


@app.errorhandler(ParamsValueError)
def params_value_error(e):
    return pre.fmt_resp(e)


@app.route("/email", methods=["GET", "POST"])
def example_email_handler():
    params = pre.parse(get=email_params)
    return json_resp(params)


class TestParse:

    def test_parse_smoke(self):
        resp = app.test_client().get("/email", data={
            "params": "wudong@eastwu.cn"
        })
        assert resp.json == {"params": "wudong@eastwu.cn"}

    def test_parse_error(self):
        resp = app.test_client().get("/email", data={
            "params": "wudong@@eastwu.cn"
        })
        assert resp.json["respMsg"] == "'params' does not match the regular expression"
