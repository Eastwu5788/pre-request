# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2020
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-12-21 13:07'
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
    "userFirst": {
        "userId": Rule(type=int, required=False),
        "socialInfo": {
            "gender": Rule(type=int, enum=[1, 2], default=1),
            "age": Rule(type=int, gte=18, lt=80),
            "country": Rule(required=True, deep=False)
        }
    }
}


@app.route("/structure", methods=["GET", "POST"])
@pre.catch(args)
def structure_handler(params):
    return json_resp(params)


class TestComplexStructure:

    def test_structure_smoke(self):
        """ 冒烟测试
        """
        params = {
            "userFirst": {
                "userId": 14,
            }
        }
        resp = app.test_client().post("/structure", json=params)
        assert resp.json["respMsg"] == "'userFirst.socialInfo.gender' can't be empty"
