# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2021
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '4/9/21 10:45 AM'
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
    "userIds": Rule(type=int, required=False, default=None, multi=True)
}


@app.route("/userIds", methods=["GET", "POST"])
@pre.catch(args)
def user_id_handler(params):
    return json_resp(params)


if __name__ == "__main__":
    params = {
    }
    resp = app.test_client().post("/userIds", json=params)
    print(resp.json)
