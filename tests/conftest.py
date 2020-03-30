# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2019
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-03-17 16:02'
import json

import pytest
from flask import Flask
from flask import make_response

from pre_request import filter_params
from pre_request import Rule


app = Flask(__name__)


def json_resp(result):
    result = json.dumps(result)
    resp = make_response(result)
    resp.headers['Content-Type'] = 'application/json'
    return resp


email_params = {
    "email": Rule(email=True)
}


@app.route("/email", methods=['get', 'post'])
@filter_params(email_params)
def test_email_handler(params):
    """ 测试邮件验证
    """
    return json_resp(params)


empty_params = {
    "int": Rule(allow_empty=False),
    "str": Rule(allow_empty=False),
    "str2": Rule(allow_empty=True),
    "int2": Rule(allow_empty=True, default=1)
}


@app.route("/empty", methods=['get', 'post'])
@filter_params(empty_params)
def test_empty_handler(params):
    """ 测试缺失判断验证
    """
    return json_resp(params)


enum_params = {
    "params": Rule(direct_type=int, enum=[1, 2, 3]),
    "params2": Rule(direct_type=str, enum=["a", "b", "c"])
}


@app.route("/enum", methods=['get', 'post'])
@filter_params(enum_params)
def test_enum_handler(params):
    """ 测试枚举判断验证
    """
    return json_resp(params)


json_params = {
    "params": Rule(json=True)
}


@app.route("/json", methods=['get', 'post'])
@filter_params(json_params)
def test_json_handler(params):
    """ 测试JSON转换
    """
    return json_resp(params)


length_params = {
    "params": Rule(gt=1, lt=3),
    "params2": Rule(gte=3, lte=3)
}


@app.route("/length", methods=['get', 'post'])
@filter_params(length_params)
def test_length_handler(params):
    """ 测试JSON转换
    """
    return json_resp(params)


mobile_params = {
    "params": Rule(mobile=True)
}


@app.route("/mobile", methods=['get', 'post'])
@filter_params(mobile_params)
def test_mobile_handler(params):
    """ 测试JSON转换
    """
    return json_resp(params)


range_params = {
    "params": Rule(direct_type=int, gt=10, lt=20),
    "params2": Rule(direct_type=int, gte=10, lte=10)
}


@app.route("/range", methods=['get', 'post'])
@filter_params(range_params)
def test_range_handler(params):
    """ 测试JSON转换
    """
    return json_resp(params)


eq_params = {
    "p1": Rule(direct_type=int, eq=1),
    "p2": Rule(eq="1"),
    "p3": Rule(direct_type=int, neq=1),
    "p4": Rule(neq="1")
}


@app.route("/equal", methods=['get', 'post'])
@filter_params(eq_params)
def test_eq_handler(params):
    """ 测试eq判断
    """
    return json_resp(params)


regexp_params = {
    "params": Rule(reg=r"^[1-9]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1])$")
}


@app.route("/regexp", methods=['get', 'post'])
@filter_params(regexp_params)
def test_regexp_handler(params):
    """ 测试JSON转换
    """
    return json_resp(params)


trim_params = {
    "params": Rule(trim=True)
}


@app.route("/trim", methods=['get', 'post'])
@filter_params(trim_params)
def test_trim_handler(params):
    """ 测试JSON转换
    """
    return json_resp(params)


type_params = {
    "int": Rule(direct_type=int),
    "str": Rule(direct_type=str)
}


@app.route("/type", methods=['get', 'post'])
@filter_params(type_params)
def test_type_handler(params):
    """ 测试JSON转换
    """
    return json_resp(params)


def call_back_func(value):
    if value == "3":
        return 999
    return value


callback_params = {
    "params": Rule(direct_type=str, callback=call_back_func)
}


@app.route("/callback", methods=['get', 'post'])
@filter_params(callback_params)
def test_callback_handler(params):
    """ 测试JSON转换
    """
    return json_resp(params)


key_map_params = {
    "params": Rule(direct_type=str, key_map="ttt")
}


@app.route("/keymap", methods=['get', 'post'])
@filter_params(key_map_params)
def test_keymap_handler(params):
    """ 测试JSON转换
    """
    return json_resp(params)


@pytest.fixture
def client():
    """ 构建测试用例
    """
    app.config["TESTING"] = True
    return app.test_client()
