# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2021
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2022/2/23 9:58 上午'
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
    "id": Rule(type=int, enum=[1, 2], required=False)
}


@app.route("/userId", methods=["GET", "POST"])
def user_id_handler():
    params = pre.parse(args)
    return json_resp(params)


if __name__ == "__main__":
    resp = app.test_client().get("/userId?id=")
    print(resp.json)
