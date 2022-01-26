# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2020
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-04-28 10:15'
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
    "params": Rule(reg=r'^[A-Za-z\d]+([-_.][A-Za-z\d]+)*@([A-Za-z\d]+[-.])+[A-Za-z\d]{2,4}$')
}


@app.route("/email", methods=["GET", "POST"])
@pre.catch(args)
def example_storage_handler(test_params):
    return json_resp(test_params)


class TestStoreKey:

    def test_store_key(self):
        pre.store_key = "test_params"

        resp = app.test_client().get("/email", data={
            "params": "wudong@eastwu.cn"
        })

        pre.store_key = "params"
        assert resp.json == {"params": "wudong@eastwu.cn"}
