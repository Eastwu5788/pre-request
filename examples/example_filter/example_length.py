# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2020
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-03-19 10:49'
""" 演示 pre-request 框架如何使用长度校验，仅针对字符串有效
"""
import json

from flask import Flask
from pre_request import filter_params, Rule


app = Flask(__name__)
app.config["TESTING"] = True
client = app.test_client()


# 指定email=True，此时框架会自动判断用户入参是否符合email正则
length_params = {
    "params": Rule(gt=2, lt=4)
}


@app.route("/length", methods=["GET", "POST"])
@filter_params(length_params)
def example_length_handler(params):
    return str(params)


def example_length_filter():
    """ 演示字符串长度验证
    """
    resp = client.get("/length", data={
        "params": "abc"
    })
    print(resp.data)

    resp = client.get("/length", data={
        "params": "a"
    })
    print(json.loads(resp.data))

    resp = client.get("/length", data={
        "params": "abcde"
    })
    print(json.loads(resp.data))


if __name__ == "__main__":
    example_length_filter()
