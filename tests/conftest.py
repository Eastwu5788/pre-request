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


g_params = {
    "email": Rule(email=True)
}


@app.route("/g", methods=['get', 'post'])
@pre.catch(g_params)
def test_g_handler():
    """ 测试邮件验证
    """
    from flask import g
    return json_resp(g.params)


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
    "params": Rule(type=int, enum=[1, 2, 3]),
    "params2": Rule(type=str, enum=["a", "b", "c"])
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
    "params": Rule(type=int, gt=10, lt=20),
    "params2": Rule(type=int, gte=10, lte=10)
}


@app.route("/range", methods=['get', 'post'])
@pre.catch(range_params)
def test_range_handler(params):
    """ 测试int类型数据范围校验
    """
    return json_resp(params)


eq_params = {
    "p1": Rule(type=int, eq=1),
    "p2": Rule(eq="1"),
    "p3": Rule(type=int, neq=1),
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
    "int": Rule(type=int),
    "str": Rule(type=str)
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
    "params": Rule(type=str, callback=call_back_func)
}


@app.route("/callback", methods=['get', 'post'])
@pre.catch(callback_params)
def test_callback_handler(params):
    """ 测试自定义处理callback校验
    """
    return json_resp(params)


key_map_params = {
    "params": Rule(type=str, dest="ttt")
}


@app.route("/keymap", methods=['get', 'post'])
@pre.catch(key_map_params)
def test_keymap_handler(params):
    """ 测试key映射校验
    """
    return json_resp(params)


skip_params = {
    "v1": Rule(skip=True, type=float, required=False, default=30.0),
    "v2": Rule(skip=False, type=float, required=False, default=30.0),
}


@app.route("/skip", methods=['get', 'post'])
@pre.catch(skip_params)
def test_skip_handler(params):
    """ 测试 skip 功能
    """
    return json_resp(params)


required_with_params = {
    "p1": Rule(required=False),
    "p2": Rule(required=False, required_with="p1", type=float)
}


@app.route("/required/with", methods=["GET", "POST"])
@pre.catch(required_with_params)
def test_required_with_handler(params):
    return json_resp(params)


# 指定 contains 数组，则要求入参必须包含指定子串
contains_params = {
    "p1": Rule(contains=["a", "b", "c"])
}


@app.route("/contains", methods=["GET", "POST"])
@pre.catch(contains_params)
def test_contains_handler(params):
    return json_resp(params)


# 指定 contains_any 数组，则要求入参包含任意指定子串
contains_any_params = {
    "p1": Rule(contains_any=["a", "c"])
}


@app.route("/contains/any", methods=["GET", "POST"])
@pre.catch(contains_any_params)
def test_contains_any_handler(params):
    return json_resp(params)


# 指定excludes数组，则要求入参必须禁止包含指定子串
excludes_params = {
    "p1": Rule(excludes=["a", "b", "c"])
}


@app.route("/excludes", methods=["GET", "POST"])
@pre.catch(excludes_params)
def test_excludes_handler(params):
    return json_resp(params)


# 指定contains数组，则要求入参必须包含指定子串
startswith_params = {
    "p1": Rule(startswith="abc")
}


@app.route("/startswith", methods=["GET", "POST"])
@pre.catch(startswith_params)
def test_startswith_handler(params):
    return json_resp(params)


# 指定endswith，验证字符串是否包含指定后缀
endswith_params = {
    "p1": Rule(endswith="abc")
}


@app.route("/endswith", methods=["GET", "POST"])
@pre.catch(endswith_params)
def test_endswith_handler(params):
    return json_resp(params)


# 指定lower，字符串将被转换成小写
lower_params = {
    "p1": Rule(lower=True)
}


@app.route("/lower", methods=["GET", "POST"])
@pre.catch(lower_params)
def test_lower_handler(params):
    return json_resp(params)


# upper，字符串将被转换成大写
upper_params = {
    "p1": Rule(upper=True)
}


@app.route("/upper", methods=["GET", "POST"])
@pre.catch(upper_params)
def test_upper_handler(params):
    return json_resp(params)


# ipv4，框架将验证入参是否符合ipv4规则
ipv4_params = {
    "p1": Rule(ipv4=True)
}


@app.route("/ipv4", methods=["GET", "POST"])
@pre.catch(ipv4_params)
def test_ipv4_handler(params):
    return json_resp(params)


# ipv6，框架将验证入参是否符合ipv6规则
ipv6_params = {
    "p1": Rule(ipv6=True)
}


@app.route("/ipv6", methods=["GET", "POST"])
@pre.catch(ipv6_params)
def test_ipv6_handler(params):
    return json_resp(params)


# mac，框架将验证入参是否符合mac规则
mac_params = {
    "p1": Rule(mac=True)
}


@app.route("/mac", methods=["GET", "POST"])
@pre.catch(mac_params)
def test_mac_handler(params):
    return json_resp(params)


# latitude，框架将验证入参是否符合地理纬度规则
latitude_params = {
    "p1": Rule(latitude=True)
}


@app.route("/latitude", methods=["GET", "POST"])
@pre.catch(latitude_params)
def test_latitude_handler(params):
    return json_resp(params)


# longitude，框架将验证入参是否符合地理纬度规则
longitude_params = {
    "p1": Rule(longitude=True)
}


@app.route("/longitude", methods=["GET", "POST"])
@pre.catch(longitude_params)
def test_longitude_handler(params):
    return json_resp(params)


# 指定eq_key, 邀请
eq_key_params = {
    "p1": Rule(type=int),
    "p2": Rule(type=int, eq_key="p1")
}


@app.route("/eq/key", methods=["GET", "POST"])
@pre.catch(eq_key_params)
def test_eq_key_handler(params):
    return json_resp(params)


# 指定neq_key, 禁止两个参数相等
neq_key_params = {
    "p1": Rule(type=int),
    "p2": Rule(type=int, neq_key="p1")
}


@app.route("/neq/key", methods=["GET", "POST"])
@pre.catch(neq_key_params)
def test_neq_key_handler(params):
    return json_resp(params)


# 指定gt_key, 禁止两个参数相等
gt_key_params = {
    "p1": Rule(type=int),
    "p2": Rule(type=int, gt_key="p1")
}


@app.route("/gt/key", methods=["GET", "POST"])
@pre.catch(gt_key_params)
def test_gt_key_handler(params):
    return json_resp(params)


# 指定gte_key, 禁止两个参数相等
gte_key_params = {
    "p1": Rule(type=int),
    "p2": Rule(type=int, gte_key="p1")
}


@app.route("/gte/key", methods=["GET", "POST"])
@pre.catch(gte_key_params)
def test_gte_key_handler(params):
    return json_resp(params)


# 指定lt_key, 限定一个参数必须小于另一个参数
lt_key_params = {
    "p1": Rule(type=int),
    "p2": Rule(type=int, lt_key="p1")
}


@app.route("/lt/key", methods=["GET", "POST"])
@pre.catch(lt_key_params)
def test_lt_key_handler(params):
    return json_resp(params)


# 指定lte_key, 限定一个参数必须小于另一个参数
lte_key_params = {
    "p1": Rule(type=int),
    "p2": Rule(type=int, lte_key="p1")
}


@app.route("/lte/key", methods=["GET", "POST"])
@pre.catch(lte_key_params)
def test_lte_key_handler(params):
    return json_resp(params)


@pytest.fixture
def client():
    """ 构建测试用例
    """
    app.config["TESTING"] = True
    return app.test_client()
