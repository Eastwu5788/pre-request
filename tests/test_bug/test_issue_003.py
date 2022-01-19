# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2020
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-11-13 10:53'
# sys
import json
import datetime
from decimal import Decimal
# 3p
from flask import Flask, make_response
# project
from pre_request import pre, Rule


app = Flask(__name__)
app.config["TESTING"] = True


class JSONEncoder(json.JSONEncoder):

    def default(self, o):  # pylint: disable=method-hidden

        # 处理datetime
        if isinstance(o, datetime.datetime):
            return o.strftime("%Y-%m-%d %H:%M:%S")

        # 处理日期
        if isinstance(o, datetime.date):
            return o.strftime("%Y-%m-%d")

        # 处理decimal
        if isinstance(o, Decimal):
            return float(o)

        # 其它默认处理
        return json.JSONEncoder.default(self, o)


def json_resp(result):
    result = json.dumps(result, cls=JSONEncoder)
    resp = make_response(result)
    resp.headers['Content-Type'] = 'application/json'
    return resp


# 验证Decimal类型数据的范围检验
range_params = {
    "p1": Rule(type=Decimal, gt=Decimal(0), lt=Decimal(20)),
    "p2": Rule(type=Decimal, gte=Decimal(2), lte=Decimal(5))
}


@app.route("/range/decimal", methods=["GET", "POST"])
@pre.catch(range_params)
def gte_key_handler(params):
    return json_resp(params)


class TestRangeDecimal:

    def test_range_decimal_smoke(self):
        """ 冒烟测试
        """
        resp = app.test_client().get("/range/decimal", data={
            "p1": 10,
            "p2": 2
        })
        assert resp.json == {"p1": 10.0, "p2": 2.0}

    def test_range_decimal_568(self):
        """ 测试范围异常
        """

        resp = app.test_client().get("/range/decimal", data={
            "p1": 0,
            "p2": 2
        })
        assert resp.json["respMsg"] == "p1 field value must be greater than 0"

    def test_range_decimal_572(self):
        """ 测试范围异常 572
        :return:
        """
        resp = app.test_client().get("/range/decimal", data={
            "p1": 20,
            "p2": 5
        })
        assert resp.json["respMsg"] == "p1 field value must be less than 20"
