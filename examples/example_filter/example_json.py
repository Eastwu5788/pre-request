# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2020
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-03-19 10:33'
""" 演示 pre-request 框架如何使用Json校验
"""
import json
from flask import Flask
from pre_request import pre, Rule


app = Flask(__name__)
app.config["TESTING"] = True
client = app.test_client()


# json=True，此时框架会自动将params数据进行json解析
json_params = {
    "params": Rule(json=True)
}


@app.route("/json", methods=["GET", "POST"])
@pre.catch(json_params)
def example_json_handler(params):
    return str(params)


def example_json_filter():
    """ 演示邮箱验证
    """
    resp = client.post("/json", json={
        "params": json.dumps(["hello", "work", "!"])
    })
    print(resp.data)


if __name__ == "__main__":
    example_json_filter()
