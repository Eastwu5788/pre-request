# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2020
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-04-13 10:53'
""" 演示 pre-request 框架验证字符串大写测试
"""
from flask import Flask
from pre_request import pre, Rule


app = Flask(__name__)
app.config["TESTING"] = True
client = app.test_client()


# upper，字符串将被转换成大写
upper_params = {
    "p1": Rule(upper=True)
}


@app.route("/upper", methods=["GET", "POST"])
@pre.catch(upper_params)
def example_upper_handler(params):
    return str(params)


def example_upper_filter():
    """ 演示upper字符串后缀能力
    """
    resp = client.get("/upper", data={
        "p1": "test"
    })
    print(resp.data)


if __name__ == "__main__":
    example_upper_filter()
