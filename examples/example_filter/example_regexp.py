# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2020
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-03-19 11:02'
""" 演示 pre-request 框架如何使用正则表达式验证
"""
from flask import Flask
from pre_request import pre, Rule


app = Flask(__name__)
app.config["TESTING"] = True
client = app.test_client()


# 指定 reg 可以自定义正则表达式
regexp_params = {
    "params": Rule(reg=r"^[1-9]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1])$")
}


@app.route("/regexp", methods=["GET", "POST"])
@pre.catch(regexp_params)
def example_regexp_handler(params):
    return str(params)


def example_regexp_filter():
    """ 演示邮箱验证
    """
    resp = client.get("/regexp", data={
        "params": "2019-09-01"
    })
    print(resp.data)

    resp = client.get("/regexp", data={
        "params": "2019-09-021"
    })
    print(resp.data)


if __name__ == "__main__":
    example_regexp_filter()
