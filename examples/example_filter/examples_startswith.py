# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2020
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-04-13 10:52'
""" 演示 pre-request 框架验证指定字符串前缀测试
"""
from flask import Flask
from pre_request import pre, Rule


app = Flask(__name__)
app.config["TESTING"] = True
client = app.test_client()


# 指定contains数组，则要求入参必须包含指定子串
startswith_params = {
    "p1": Rule(startswith="abc")
}


@app.route("/startswith", methods=["GET", "POST"])
@pre.catch(startswith_params)
def example_contains_handler(params):
    return str(params)


def example_startswith_filter():
    """ 演示startswith字符串前缀能力
    """
    resp = client.get("/startswith", data={
        "p1": "abcTest"
    })
    print(resp.data)

    resp = client.get("/startswith", data={
        "p1": "acTest"
    })
    print(resp.data)


if __name__ == "__main__":
    example_startswith_filter()
