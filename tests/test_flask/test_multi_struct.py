# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2020
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-12-22 13:03'
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


class TestMultiStructure:

    def test_multi_structure_smoke(self):
        """ 冒烟测试
        """
        params = {
            "userInfo": [
                {
                    "userId": 12,
                    "userName": "张三",
                    "friends": [{
                        "userId": 18,
                        "userName": "王五"
                    }]

                }
            ]
        }
        resp = app.test_client().get("/structure", json=params)
        assert resp.json == params

    def test_multi_structure_560(self):
        """ 冒烟测试
        """
        params = {
            "userInfo": {}
        }
        resp = app.test_client().get("/structure", json=params)
        assert resp.json["respMsg"] == "userInfo field cannot be empty"

    def test_multi_structure_601(self):
        """ 冒烟测试
        """
        params = {
            "userInfo": {
                "test": "value"
            }
        }
        resp = app.test_client().get("/structure", json=params)
        assert resp.json["respMsg"] == "Input userInfo invalid type"

    def test_multi_structure_562(self):
        """ 冒烟测试
        """
        params = {
            "userInfo": [
                {
                    "userId": "t"
                }
            ]
        }
        resp = app.test_client().get("/structure", json=params)
        assert resp.json["respMsg"] == "'userInfo.0.userId' can't convert to 'int' type"

    def test_multi_structure_563(self):
        """ 测试560异常
        """
        params = {
            "userInfo": [
                {
                    "userId": 13,
                    "userName": "张三",
                    "friends": [

                    ]
                }
            ]
        }
        resp = app.test_client().get("/structure", json=params)
        assert resp.json["respMsg"] == "userInfo.0.friends field cannot be empty"

    def test_multi_structure_562_2(self):
        """ 测试二层562异常
        """
        params = {
            "userInfo": [
                {
                    "userId": "123",
                    "userName": "张三",
                    "friends": [
                        {
                            "userId": "s"
                        }
                    ]
                }
            ]
        }
        resp = app.test_client().get("/structure", json=params)
        assert resp.json["respMsg"] == "'userInfo.0.friends.0.userId' can't convert to 'int' type"
