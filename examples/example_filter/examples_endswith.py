# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2020
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-04-13 10:52'
""" 演示 pre-request 框架验证指定字符串后缀测试
"""
from flask import Flask
from pre_request import pre, Rule


app = Flask(__name__)
app.config["TESTING"] = True
client = app.test_client()


# 指定endswith，验证字符串是否包含指定后缀
endswith_params = {
    "p1": Rule(endswith="abc")
}


@app.route("/endswith", methods=["GET", "POST"])
@pre.catch(endswith_params)
def example_endswith_handler(params):
    return str(params)


def example_endswith_filter():
    """ 演示endswith字符串后缀能力
    """
    resp = client.get("/endswith", data={
        "p1": "Testabc"
    })
    print(resp.data)

    resp = client.get("/endswith", data={
        "p1": "Testac"
    })
    print(resp.data)


if __name__ == "__main__":
    example_endswith_filter()
