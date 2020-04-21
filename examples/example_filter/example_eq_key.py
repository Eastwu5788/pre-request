# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2020
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-04-13 10:54'
""" 演示 pre-request 框架验证不同参数联动相等
"""
from flask import Flask
from pre_request import pre, Rule


app = Flask(__name__)
app.config["TESTING"] = True
client = app.test_client()


# 指定eq_key, 邀请
eq_key_params = {
    "p1": Rule(type=int),
    "p2": Rule(type=int, eq_key="p1")
}


@app.route("/eq/key", methods=["GET", "POST"])
@pre.catch(eq_key_params)
def example_eq_key_handler(params):
    return str(params)


def example_eq_key_filter():
    """ 演示eq_key包含函数
    """
    resp = client.get("/eq/key", data={
        "p1": 15,
        "p2": 15
    })
    print(resp.data)


if __name__ == "__main__":
    example_eq_key_filter()
