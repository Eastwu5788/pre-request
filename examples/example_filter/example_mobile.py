# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2020
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-03-19 10:54'
""" 演示 pre-request 框架如何使用手机号校验

目前使用的正则表达式为: ^0\d{2,3}\d{7,8}$|^1[3578]\d{9}$|^14[579]\d{8}$
"""
from flask import Flask
from pre_request import filter_params, Rule


app = Flask(__name__)
app.config["TESTING"] = True
client = app.test_client()


# 指定mobile=True，此时框架会自动判断用户入参是否符合mobile正则
mobile_params = {
    "params": Rule(mobile=True)
}


@app.route("/mobile", methods=["GET", "POST"])
@filter_params(mobile_params)
def example_mobile_handler(params):
    return str(params)


def example_mobile_filter():
    """ 演示手机号验证
    """
    resp = client.get("/mobile", data={
        "params": "13899991111"
    })
    print(resp.data)


if __name__ == "__main__":
    example_mobile_filter()
