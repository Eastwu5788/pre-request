# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2020
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-08-07 10:13'
import json
from flask import Flask, make_response
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
    "userId": Rule(type=str, gte=1, lte=20, required=False, multi=True, dest="use_id_s")
}


@app.route("/bug", methods=["GET", "POST"])
@pre.catch(args)
def structure_handler(params):
    return json_resp(params)


def example_issue_001():
    """ 演示回调函数
    """
    # resp = client.get("/bug", json={
    #     "userId": [
    #         1,
    #         2
    #     ]
    # })
    # print(resp.data)

    resp = client.get("/bug", json={})
    print(resp.data)


if __name__ == "__main__":
    example_issue_001()
