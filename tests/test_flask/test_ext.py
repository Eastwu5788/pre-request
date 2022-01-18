# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2020
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-05-12 17:40'
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


@app.route("/email", methods=["GET", "POST"])
@pre.catch(args)
def example_ext_handler(test_params):
    return json_resp(test_params)


class TestFlaskExt:

    def test_flask_ext(self):
        app.config["PRE_FUZZY"] = True
        app.config["PRE_STORE_KEY"] = "test_params"
        pre.init_app(app=app)

        resp1 = app.test_client().get("/email", data={
            "params": "wudong@eastwu.cn"
        })

        resp2 = app.test_client().get("/email", data={
            "params": "",
        })

        app.config["PRE_FUZZY"] = False
        app.config["PRE_STORE_KEY"] = "params"
        pre.init_app(app=app)

        assert resp1.json == {"params": "wudong@eastwu.cn"}
        assert resp2.json == {'respCode': 464, 'respMsg': 'Parameter verification failed, please check your input',
                              'result': {}}
