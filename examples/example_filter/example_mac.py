# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2020
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-04-13 10:53'
""" 演示 pre-request 框架验证字符串是否符合mac硬件地址格式
"""
from flask import Flask
from pre_request import pre, Rule


app = Flask(__name__)
app.config["TESTING"] = True
client = app.test_client()


# mac，框架将验证入参是否符合mac规则
mac_params = {
    "p1": Rule(mac=True)
}


@app.route("/mac", methods=["GET", "POST"])
@pre.catch(mac_params)
def example_mac_handler(params):
    return str(params)


def example_mac_filter():
    """ 演示mac格式判断能力
    """
    resp = client.get("/mac", data={
        "p1": "34:29:8f:98:16:e4"
    })
    print(resp.data)


if __name__ == "__main__":
    example_mac_filter()
