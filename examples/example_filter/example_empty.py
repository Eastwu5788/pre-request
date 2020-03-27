# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2020
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-03-19 10:23'
""" 演示 pre-request 框架如何使用空值校验
"""
from flask import Flask
from pre_request import filter_params, Rule


app = Flask(__name__)
app.config["TESTING"] = True
client = app.test_client()


# 指定email=True，此时框架会自动判断用户入参是否符合email正则
empty_params = {
    "params": Rule(allow_empty=True, default="tmp"),
    "must": Rule(allow_empty=False)
}


@app.route("/empty", methods=["GET", "POST"])
@filter_params(empty_params)
def example_empty_handler(params):
    return str(params)


def example_empty_filter():
    """ 演示邮箱验证
    """
    resp = client.get("/empty", data={
        "params": "wudong@eastwu.cn",
        "must": "must"
    })
    print(resp.data)

    # params参数不传时，会默认填充default值
    resp = client.get("/empty", data={
        "must": "must",
    })
    print(resp.data)

    # 不允许为空的值如果不填写会报错
    resp = client.get("/empty", data={
        "params": "ss"
    })
    print(resp.data)


if __name__ == "__main__":
    example_empty_filter()
