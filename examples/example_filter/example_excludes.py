# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2020
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-04-13 10:52'
""" 演示 pre-request 框架验证字符串禁止包含测试
"""
from flask import Flask
from pre_request import pre, Rule


app = Flask(__name__)
app.config["TESTING"] = True
client = app.test_client()


# 指定excludes数组，则要求入参必须禁止包含指定子串
excludes_params = {
    "p1": Rule(excludes=["a", "b", "c"])
}


@app.route("/excludes", methods=["GET", "POST"])
@pre.catch(excludes_params)
def example_excludes_handler(params):
    return str(params)


def example_excludes_filter():
    """ 演示contains包含函数
    """
    resp = client.get("/excludes", data={
        "p1": "aoe"
    })
    print(resp.data)


if __name__ == "__main__":
    example_excludes_filter()
