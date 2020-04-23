# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2020
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-04-13 10:55'
""" 演示 pre-request 框架验证不同参数联动限制禁止相等
"""
import json
from flask import Flask
from pre_request import pre, Rule


app = Flask(__name__)
app.config["TESTING"] = True
client = app.test_client()


# 指定lte_key, 限定一个参数必须小于另一个参数
lte_key_params = {
    "p1": Rule(type=int),
    "p2": Rule(type=int, lte_key="p1")
}


@app.route("/lte/key", methods=["GET", "POST"])
@pre.catch(lte_key_params)
def example_lte_key_handler(params):
    return str(params)


def example_lte_key_filter():
    """ 演示lte_key包含函数
    """
    resp = client.get("/lte/key", data={
        "p1": 15,
        "p2": 16
    })
    print(json.loads(resp.data))

    resp = client.get("/lte/key", data={
        "p1": 15,
        "p2": 15
    })
    print(resp.data)


if __name__ == "__main__":
    example_lte_key_filter()
