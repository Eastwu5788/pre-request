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

from pre_request import pre
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
@pre.catch(email_params)
def test_email_handler(params):
    """ 测试邮件验证
    """
    return json_resp(params)


empty_params = {
    "int": Rule(required=True),
    "str": Rule(required=True),
    "str2": Rule(required=False),
    "int2": Rule(required=False, default=1)
}


@app.route("/empty", methods=['get', 'post'])
@pre.catch(empty_params)
def test_empty_handler(params):
    """ 测试缺失判断验证
    """
    return json_resp(params)


enum_params = {
    "params": Rule(direct_type=int, enum=[1, 2, 3]),
    "params2": Rule(direct_type=str, enum=["a", "b", "c"])
}


@app.route("/enum", methods=['get', 'post'])
@pre.catch(enum_params)
def test_enum_handler(params):
    """ 测试枚举判断验证
    """
    return json_resp(params)


json_params = {
    "params": Rule(json=True)
}


@app.route("/json", methods=['get', 'post'])
@pre.catch(json_params)
def test_json_handler(params):
    """ 测试JSON转换
    """
    return json_resp(params)


length_params = {
    "params": Rule(gt=1, lt=3),
    "params2": Rule(gte=3, lte=3)
}


@app.route("/length", methods=['get', 'post'])
@pre.catch(length_params)
def test_length_handler(params):
    """ 测试字符串数据长度校验
    """
    return json_resp(params)


mobile_params = {
    "params": Rule(mobile=True)
}


@app.route("/mobile", methods=['get', 'post'])
@pre.catch(mobile_params)
def test_mobile_handler(params):
    """ 测试手机号格式校验
    """
    return json_resp(params)


range_params = {
    "params": Rule(direct_type=int, gt=10, lt=20),
    "params2": Rule(direct_type=int, gte=10, lte=10)
}


@app.route("/range", methods=['get', 'post'])
@pre.catch(range_params)
def test_range_handler(params):
    """ 测试int类型数据范围校验
    """
    return json_resp(params)


eq_params = {
    "p1": Rule(direct_type=int, eq=1),
    "p2": Rule(eq="1"),
    "p3": Rule(direct_type=int, neq=1),
    "p4": Rule(neq="1")
}


@app.route("/equal", methods=['get', 'post'])
@pre.catch(eq_params)
def test_eq_handler(params):
    """ 测试eq判断
    """
    return json_resp(params)


regexp_params = {
    "params": Rule(reg=r"^[1-9]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1])$")
}


@app.route("/regexp", methods=['get', 'post'])
@pre.catch(regexp_params)
def test_regexp_handler(params):
    """ 测试正则校验
    """
    return json_resp(params)


trim_params = {
    "params": Rule(trim=True)
}


@app.route("/trim", methods=['get', 'post'])
@pre.catch(trim_params)
def test_trim_handler(params):
    """ 测试去除前后空格校验
    """
    return json_resp(params)


type_params = {
    "int": Rule(direct_type=int),
    "str": Rule(direct_type=str)
}


@app.route("/type", methods=['get', 'post'])
@pre.catch(type_params)
def test_type_handler(params):
    """ 测试字段目标数据类型校验
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
@pre.catch(callback_params)
def test_callback_handler(params):
    """ 测试自定义处理callback校验
    """
    return json_resp(params)


key_map_params = {
    "params": Rule(direct_type=str, key_map="ttt")
}


@app.route("/keymap", methods=['get', 'post'])
@pre.catch(key_map_params)
def test_keymap_handler(params):
    """ 测试key映射校验
    """
    return json_resp(params)


@pytest.fixture
def client():
    """ 构建测试用例
    """
    app.config["TESTING"] = True
    return app.test_client()
