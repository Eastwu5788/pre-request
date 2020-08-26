# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2020
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-04-28 10:58'
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


# 指定email=True，此时框架会自动判断用户入参是否符合email正则
args = {
    "params": Rule(email=True)
}


@app.route("/fuzzy", methods=["GET", "POST"])
@pre.catch(args)
def example_fuzzy_handler(params):
    return json_resp(params)


class TestStoreKey:

    def test_store_key(self):
        pre.fuzzy = True

        resp = app.test_client().get("/fuzzy", data={
            "params": "wudong@@eastwu.cn"
        })

        pre.fuzzy = False
        assert resp.json == {"respCode": 564, "respMsg": "Parameter verification failed, please check your input",
                             "result": {}}
