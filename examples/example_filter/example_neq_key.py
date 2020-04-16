# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2020
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-04-13 10:54'
""" 演示 pre-request 框架验证不同参数联动限制禁止相等
"""
from flask import Flask
from pre_request import pre, Rule


app = Flask(__name__)
app.config["TESTING"] = True
client = app.test_client()


# 指定neq_key, 禁止两个参数相等
neq_key_params = {
    "p1": Rule(direct_type=int),
    "p2": Rule(direct_type=int, neq_key="p1")
}


@app.route("/neq/key", methods=["GET", "POST"])
@pre.catch(neq_key_params)
def example_neq_key_handler(params):
    return str(params)


def example_neq_key_filter():
    """ 演示neq_key包含函数
    """
    resp = client.get("/neq/key", data={
        "p1": 15,
        "p2": 16
    })
    print(resp.data)


if __name__ == "__main__":
    example_neq_key_filter()
