# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2020
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-03-19 11:15'
""" 演示 pre-request 框架如何使用回调函数自定义处理函数
"""
from flask import Flask
from pre_request import pre, Rule


app = Flask(__name__)
app.config["TESTING"] = True
client = app.test_client()


def call_back_handler(value):
    return value + 100


# 指定callback自定义处理函数，注意：此函数的调用在系统处理完之后
callback_params = {
    "params": Rule(type=int, callback=call_back_handler)
}


@app.route("/callback", methods=["GET", "POST"])
@pre.catch(callback_params)
def example_callback_handler(params):
    return str(params)


def example_callback_filter():
    """ 演示回调函数
    """
    resp = client.get("/callback", data={
        "params": 10
    })
    print(resp.data)


if __name__ == "__main__":
    example_callback_filter()
