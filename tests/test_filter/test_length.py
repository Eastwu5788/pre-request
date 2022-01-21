# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2020
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-03-18 10:42'
import json
from flask import make_response, Flask
from pre_request import pre, Rule


app = Flask(__name__)
app.config["TESTING"] = True


rule = {
    "params": Rule(gt=1, lt=3),
    "params2": Rule(gte=3, lte=3),
    "p3": Rule(len=3, required=False, default="1")
}


@app.route("/length", methods=['GET', 'POST'])
@pre.catch(rule)
def length_handler(params):
    """ 测试字符串数据长度校验
    """
    result = json.dumps(params)
    resp = make_response(result)
    resp.headers['Content-Type'] = 'application/json'
    return resp


class TestLength:

    def test_length_filter_smoke(self):
        """ 测试 length_filter 过滤器
        """
        resp = app.test_client().get("/length", data={
            "params": "ta",
            "params2": "aaa"
        })

        assert resp.json == {"params": "ta", "params2": "aaa", "p3": "1"}

    def test_length_filter_574(self):
        """ 测试 length_filter 574 错误
        """

        resp = app.test_client().get("/length", data={
            "params": "h",
            "params2": "aaa"
        })
        assert resp.json["respMsg"] == "the length of 'params' should be greater than 1"

    def test_length_filter_575(self):
        """ 测试 length_filter 575 错误
        """

        resp = app.test_client().get("/length", data={
            "params": "he",
            "params2": "aa"
        })
        assert resp.json["respMsg"] == "the length of 'params2' should be greater than or equal to 3"

    def test_length_filter_576(self):
        """ 测试 length_filter 576 错误
        """

        resp = app.test_client().get("/length", data={
            "params": "hello",
            "params2": "aaa"
        })
        assert resp.json["respMsg"] == "the length of 'params' should be less than 3"

    def test_length_filter_577(self):
        """ 测试 length_filter 577 错误
        """

        resp = app.test_client().get("/length", data={
            "params": "he",
            "params2": "jerry"
        })
        assert resp.json["respMsg"] == "the length of 'params2' should be less than or equal to 3"

    def test_length_filter_1(self):
        resp = app.test_client().get("/length", data={
            "params": "ta",
            "params2": "aaa",
            "p3": "12"
        })
        assert resp.json["respMsg"] == "the length of 'p3' should be equal to 3"
