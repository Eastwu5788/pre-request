# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2020
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-03-19 11:04'
""" 演示 pre-request 框架如何使用trim参数自动去除字符串首尾空格
"""
from flask import Flask
from pre_request import filter_params, Rule


app = Flask(__name__)
app.config["TESTING"] = True
client = app.test_client()


# trim=True，此时框架会自动将参数字符串首尾空格去除
trim_params = {
    "params": Rule(trim=True)
}


@app.route("/trim", methods=["GET", "POST"])
@filter_params(trim_params)
def example_trim_handler(params):
    return str(params)


def example_trim_filter():
    """ 演示去空格验证
    """
    resp = client.get("/trim", data={
        "params": " wudong@eastwu.cn "
    })
    print(resp.data)


if __name__ == "__main__":
    example_trim_filter()
