# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2021
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2022/1/24 11:20 上午'

import json
from flask import make_response, Flask
from pre_request import pre, Rule


app = Flask(__name__)
app.config["TESTING"] = True


def json_resp(result):
    result = json.dumps(result)
    resp = make_response(result)
    resp.headers['Content-Type'] = 'application/json'
    return resp


args = {
    "p1": Rule(type=str, not_startswith="USA"),
    "p2": Rule(type=str, not_endswith="USA")
}


@app.route("/not/startswith", methods=["GET", "POST"])
@pre.catch(args)
def not_se_handler(params):
    return json_resp(params)


class TestString:

    def test_not_startswith_smoke(self):
        resp = app.test_client().post("/not/startswith", data={
            "p1": "T1",
            "p2": "T2"
        })

        assert resp.json == {"p1": "T1", "p2": "T2"}

    def test_not_startswith(self):
        resp = app.test_client().post("/not/startswith", data={
            "p1": "USA-T1",
            "p2": "T2"
        })

        assert resp.json["respMsg"] == "'p1' should not start with 'USA'"

    def test_not_endswith(self):
        resp = app.test_client().post("/not/startswith", data={
            "p1": "T1",
            "p2": "T2-USA"
        })

        assert resp.json["respMsg"] == "'p2' should not end with 'USA'"
