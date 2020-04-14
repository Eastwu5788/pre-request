# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2020
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-04-13 10:52'
""" 演示 pre-request 框架验证字符串任意包含测试
"""
from flask import Flask
from pre_request import pre, Rule


app = Flask(__name__)
app.config["TESTING"] = True
client = app.test_client()


# 指定 contains_any 数组，则要求入参包含任意指定子串
contains_any_params = {
    "p1": Rule(contains_any=["a", "c"])
}


@app.route("/contains/any", methods=["GET", "POST"])
@pre.catch(contains_any_params)
def example_contains_any_handler(params):
    return str(params)


def example_contains_any_filter():
    """ 演示contains_any包含函数
    """
    resp = client.get("/contains/any", data={
        "p1": "bef"
    })
    print(resp.data)


if __name__ == "__main__":
    example_contains_any_filter()
