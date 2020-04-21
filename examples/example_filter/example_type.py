# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2020
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-03-19 11:05'
""" 演示 pre-request 框架如何使用邮箱校验
"""
import json
from flask import Flask
from pre_request import pre, Rule


app = Flask(__name__)
app.config["TESTING"] = True
client = app.test_client()


# 指定direct_type，此时框架会尝试将入参转换成目标格式
type_params = {
    "params": Rule(type=int)
}


@app.route("/type", methods=["GET", "POST"])
@pre.catch(type_params)
def example_type_handler(params):
    return json.dumps(params)


def example_type_filter():
    """ 演示邮箱验证
    """
    resp = client.get("/type", data={
        "params": 19.9
    })
    print(resp.data)

    # resp = client.get("/type", data={
    #     "params": "19"
    # })
    # print(resp.data)


if __name__ == "__main__":
    example_type_filter()
