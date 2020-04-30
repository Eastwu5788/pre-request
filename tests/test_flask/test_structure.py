# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2020
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-04-27 10:07'
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
    },
    "userSecond": {
        "userId": Rule(type=int, required=False, neq_key="userFirst.userId"),
        "socialInfo": {
            "gender": Rule(type=int, enum=[1, 2], default=1, neq_key="userFirst.socialInfo.gender"),
            "age": Rule(type=int, gte=18, lt=80, required_with="userFirst.socialInfo.age"),
            "country": Rule(required=True, deep=False)
        }
    }
}


@app.route("/structure", methods=["GET", "POST"])
@pre.catch(args)
def structure_handler(params):
    return json_resp(params)


class TestStructure:

    def test_structure_smoke(self):
        """ 测试带数据结构的参数处理
        """
        resp = app.test_client().post("/structure", json={
            "userFirst": {
                "userId": "13",
                "socialInfo": {
                    "age": 20,
                }
            },
            "userSecond": {
                "userId": 14,
                "socialInfo": {
                    "age": 21
                }
            },
            "country": "CN",
            "userFirst.socialInfo.gender": 1,
            "userSecond.socialInfo.gender": 2,
        })

        assert resp.json == {
            "userFirst": {
                "userId": 13,
                "socialInfo": {
                    "gender": 1,
                    "age": 20,
                    "country": "CN"
                }
            },
            "userSecond": {
                "userId": 14,
                "socialInfo": {
                    "gender": 2,
                    "age": 21,
                    "country": "CN"
                }
            },

        }
