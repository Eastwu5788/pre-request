# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2020
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-12-21 13:27'
import json
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
    "userInfo": Rule(type=dict, multi=True, required=True, struct={
        "userId": Rule(type=int, required=True),
        "userName": Rule(type=str, required=True),
        "friends": Rule(type=dict, multi=True, required=True, struct={
            "userId": Rule(type=int, required=True),
            "userName": Rule(type=str, required=True)
        })
    })
}


@app.route("/structure", methods=["GET", "POST"])
@pre.catch(args)
def structure_handler(params):
    return json_resp(params)


if __name__ == "__main__":
    params = {
        "userInfo": {}
    }
    resp = app.test_client().post("/structure", json=params)
    print(resp.json)
