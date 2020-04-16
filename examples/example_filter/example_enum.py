# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2020
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-03-19 10:28'
""" 演示 pre-request 框架如何使用枚举校验
"""
from flask import Flask
from pre_request import pre, Rule


app = Flask(__name__)
app.config["TESTING"] = True
client = app.test_client()


# 指定enum=[10, 20]指定目标枚举值，注意：目前仅支持同数据类型枚举验证
enum_params = {
    "params": Rule(direct_type=int, enum=[10, 20, 30])
}


@app.route("/enum", methods=["GET", "POST"])
@pre.catch(enum_params)
def example_enum_handler(params):
    return str(params)


def example_enum_filter():
    """ 演示枚举验证
    """
    resp = client.get("/enum", data={
        "params": 7
    })
    print(resp.json)


if __name__ == "__main__":
    example_enum_filter()
