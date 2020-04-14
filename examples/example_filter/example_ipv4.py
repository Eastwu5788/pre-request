# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2020
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-04-13 10:53'
""" 演示 pre-request 框架验证字符串是否符合ipv4规则
"""
from flask import Flask
from pre_request import pre, Rule


app = Flask(__name__)
app.config["TESTING"] = True
client = app.test_client()


# ipv4，框架将验证入参是否符合ipv4规则
ipv4_params = {
    "p1": Rule(ipv4=True)
}


@app.route("/ipv4", methods=["GET", "POST"])
@pre.catch(ipv4_params)
def example_ipv4_handler(params):
    return str(params)


def example_ipv4_filter():
    """ 演示ipv4格式判断能力
    """
    resp = client.get("/ipv4", data={
        "p1": "127.0.0.1"
    })
    print(resp.data)


if __name__ == "__main__":
    example_ipv4_filter()
