# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2020
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-04-13 10:53'
""" 演示 pre-request 框架验证字符串是否符合ipv6规则
"""
from flask import Flask
from pre_request import pre, Rule


app = Flask(__name__)
app.config["TESTING"] = True
client = app.test_client()


# ipv6，框架将验证入参是否符合ipv6规则
ipv6_params = {
    "p1": Rule(ipv6=True)
}


@app.route("/ipv6", methods=["GET", "POST"])
@pre.catch(ipv6_params)
def example_ipv6_handler(params):
    return str(params)


def example_ipv6_filter():
    """ 演示ipv6格式判断能力
    """
    resp = client.get("/ipv6", data={
        "p1": "CDCD:910A:2222:5498:8475:1111:3900:2020"
    })
    print(resp.data)


if __name__ == "__main__":
    example_ipv6_filter()
