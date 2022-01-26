# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2020
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-03-18 12:52'
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


regexp_params = {
    "p1": Rule(reg=r"^[1-9]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1])$", required=False, default=None),
    "p2": Rule(alpha=True, required=False, default=None),
    "p3": Rule(alphanum=True, required=False, default=None),
    "p4": Rule(email=True, required=False, default=None),
    "p5": Rule(numeric=True, required=False, default=None),
    "p6": Rule(number=True, required=False, default=None)
}


@app.route("/regexp", methods=['get', 'post'])
@pre.catch(regexp_params)
def regexp_handler(params):
    """ 测试正则校验
    """
    return json_resp(params)


regex_uri = {
    "t1": Rule(data_uri=True, required=False, default=None)
}


@app.route("/network", methods=['get', 'post'])
@pre.catch(regex_uri)
def network_handler(params):
    """ 测试正则校验
    """
    return json_resp(params)


class TestRegexp:

    def test_regexp_filter_smoke(self):
        """ 测试 regexp_filter 过滤器
        """
        resp = app.test_client().get("/regexp", data={
            "p1": "2020-03-03",
            "p2": "req",
            "p3": "req123",
            "p4": "wudong@eastwu.cn",
            "p5": "-1.2",
            "p6": "39"
        })
        assert resp.json == {"p1": "2020-03-03", "p2": "req", "p3": "req123",
                             "p4": "wudong@eastwu.cn", "p5": "-1.2", "p6": "39"}

    # def test_regex_network_smoke(self):
    #     resp = app.test_client().get("/network", data={
    #         "t1": "data:text/plain;base64,SGVsbG8sIFdvcmxkIQ==",
    #     })
    #     assert resp.json == {"t1": "data:text/plain;base64,SGVsbG8sIFdvcmxkIQ=="}

    def test_regexp_filter_566(self):
        """ 测试 regexp_filter 566 错误
        """
        resp = app.test_client().get("/regexp", data={
            "p1": "2020-3-03"
        })
        assert resp.json["respMsg"] == "'p1' does not match the regular expression"

        resp = app.test_client().get("/regexp", data={
            "p1": "2020-03"
        })
        assert resp.json["respMsg"] == "'p1' does not match the regular expression"

    def test_regex_alpha(self):
        resp = app.test_client().get("/regexp", data={
            "p2": "req-123",
        })
        assert resp.json["respMsg"] == "'p2' must consist of alpha"

    def test_regex_alphanum(self):
        resp = app.test_client().get("/regexp", data={
            "p3": "req-123",
        })
        assert resp.json["respMsg"] == "'p3' must consist of alpha or numeric"

    def test_regex_number(self):
        resp = app.test_client().get("/regexp", data={
            "p6": "123.4",
        })
        assert resp.json["respMsg"] == "'p6' must consist of number"

    def test_regex_numeric(self):
        resp = app.test_client().get("/regexp", data={
            "p5": "-123.4a",
        })
        assert resp.json["respMsg"] == "'p5' must consist of numeric"

    def test_regex_email(self):
        resp = app.test_client().get("/regexp", data={
            "p4": "@c.cn",
        })
        assert resp.json["respMsg"] == "'p4' is not a valid email address"

    # def test_regex_network_data_uri(self):
    #     resp = app.test_client().get("/network", data={
    #         "t1": "dataSGVsbG8sIFdvcmxkIQ==",
    #     })
    #     assert resp.json["respMsg"] == "'t1' is not a valid data uri"
