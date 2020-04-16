# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2020
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-04-13 10:52'
""" 演示 pre-request 框架验证字符串小写测试
"""
from flask import Flask
from pre_request import pre, Rule


app = Flask(__name__)
app.config["TESTING"] = True
client = app.test_client()


# 指定lower，字符串将被转换成小写
lower_params = {
    "p1": Rule(lower=True)
}


@app.route("/lower", methods=["GET", "POST"])
@pre.catch(lower_params)
def example_lower_handler(params):
    return str(params)


def example_lower_filter():
    """ 演示lower字符串后缀能力
    """
    resp = client.get("/lower", data={
        "p1": "TEST"
    })
    print(resp.data)


if __name__ == "__main__":
    example_lower_filter()
