# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2020
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-03-19 10:59'
""" 演示 pre-request 框架如何使用数字范围校验
"""
from flask import Flask
from pre_request import filter_params, Rule, Range


app = Flask(__name__)
app.config["TESTING"] = True
client = app.test_client()


# 指定range范围，则框架会对数字范围作出校验
range_params = {
    "params": Rule(direct_type=int, range=Range(10, 20))
}


@app.route("/range", methods=["GET", "POST"])
@filter_params(range_params)
def example_range_handler(params):
    return str(params)


def example_range_filter():
    """ 演示邮箱验证
    """
    resp = client.get("/range", data={
        "params": 12
    })
    print(resp.data)

    resp = client.get("/range", data={
        "params": 9
    })
    print(resp.data)


if __name__ == "__main__":
    example_range_filter()
