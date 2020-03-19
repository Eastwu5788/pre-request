# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2020
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-03-19 10:14'
""" 演示 pre-request 框架如何使用邮箱校验
"""
from flask import Flask
from pre_request import filter_params, Rule


app = Flask(__name__)
app.config["TESTING"] = True
client = app.test_client()


# 指定email=True，此时框架会自动判断用户入参是否符合email正则
email_params = {
    "params": Rule(email=True)
}


@app.route("/email", methods=["GET", "POST"])
@filter_params(email_params)
def example_email_handler(params):
    return str(params)


def example_email_filter():
    """ 演示邮箱验证
    """
    resp = client.get("/email", data={
        "params": "wudong@eastwu.cn"
    })
    print(resp.data)


if __name__ == "__main__":
    example_email_filter()
