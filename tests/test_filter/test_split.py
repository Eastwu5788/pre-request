# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2020
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-04-27 11:25'
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
    "p1": Rule(type=int, split=",", required=True),
    "p2": Rule(split=",", trim=True, lower=True),
    "p3": Rule(type=int, split=",", lte=5)
}


@app.route("/split", methods=["GET", "POST"])
@pre.catch(args)
def split_handler(params):
    return json_resp(params)


class TestSplit:

    def test_split_smoke(self):
        """ 测试字符串分割能力
        """
        resp = app.test_client().post("/split", data={
            "p1": "1,24,5,6,7",
            "p2": "ABC, de, cc ,F",
            "p3": "5, 2"
        })

        assert resp.json == {"p1": [1, 24, 5, 6, 7],
                             "p2": ["abc", "de", "cc", "f"],
                             "p3": [5, 2]}

    def test_split_562(self):
        """ 测试字符串分割失败情况
        """
        resp = app.test_client().post("/split", data={
            "p1": "1,a,5,6,7"
        })

        assert resp.json["respMsg"] == "'p1' can't convert to 'int' type"

    def test_split_573(self):
        """ 测试数组内数据大小限制判断
        """
        resp = app.test_client().post("/split", data={
            "p1": "1,2,5,6,7",
            "p2": "ABC, de, cc ,F",
            "p3": "5, 6"
        })

        assert resp.json["respMsg"] == "'p3' should be less than or equal to 5"
