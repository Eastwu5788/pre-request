# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2020
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-04-13 10:51'
""" 演示 pre-request 框架验证字符串包含测试
"""
from flask import Flask
from pre_request import pre, Rule


app = Flask(__name__)
app.config["TESTING"] = True
client = app.test_client()


# 指定contains数组，则要求入参必须包含指定子串
contains_params = {
    "p1": Rule(contains=["a", "b", "c"])
}


@app.route("/contains", methods=["GET", "POST"])
@pre.catch(contains_params)
def example_contains_handler(params):
    return str(params)


def example_contains_filter():
    """ 演示contains包含函数
    """
    resp = client.get("/contains", data={
        "p1": "abc"
    })
    print(resp.data)


if __name__ == "__main__":
    example_contains_filter()
