# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2020
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-04-13 10:53'
""" 演示 pre-request 框架验证字符串是否是合法的文件地址
"""
from flask import Flask
from pre_request import pre, Rule


app = Flask(__name__)
app.config["TESTING"] = True
client = app.test_client()


# 指定file，pre-request 将验证参数是否是合法的文件地址
file_params = {
    "p1": Rule(file=True)
}


@app.route("/file", methods=["GET", "POST"])
@pre.catch(file_params)
def example_file_handler(params):
    return str(params)


def example_file_filter():
    """ 演示文件地址字符串验证能力
    """
    resp = client.get("/file", data={
        "p1": "D:test"
    })
    print(resp.data)


if __name__ == "__main__":
    example_file_filter()
