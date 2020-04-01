# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2020
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-03-27 15:44'
""" 演示 pre-request 框架如何使用等于、不等于判断
"""
import json

from flask import Flask
from pre_request import pre, Rule


app = Flask(__name__)
app.config["TESTING"] = True
client = app.test_client()


equal_params = {
    "p1": Rule(direct_type=int, eq=8),
    "p2": Rule(direct_type=int, neq=8)
}


@app.route("/equal", methods=["GET", "POST"])
@pre.catch(equal_params)
def example_equal_handler(params):
    return str(params)


def example_equal_filter():
    """ 演示等于、不等于判断
    """
    resp = client.get("/equal", data={
        "p1": 8,
        "p2": 9
    })
    print(resp.data)

    resp = client.get("/equal", data={
        "p1": 9,
        "p2": 9
    })
    print(json.loads(resp.data))

    resp = client.get("/equal", data={
        "p1": 8,
        "p2": 8
    })
    print(json.loads(resp.data))


if __name__ == "__main__":
    example_equal_filter()
