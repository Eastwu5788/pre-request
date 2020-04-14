# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2020
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-04-13 10:53'
""" 演示 pre-request 框架验证字符串是否符合地理纬度坐标
"""
from flask import Flask
from pre_request import pre, Rule


app = Flask(__name__)
app.config["TESTING"] = True
client = app.test_client()


# latitude，框架将验证入参是否符合地理纬度规则
latitude_params = {
    "p1": Rule(latitude=True)
}


@app.route("/latitude", methods=["GET", "POST"])
@pre.catch(latitude_params)
def example_latitude_handler(params):
    return str(params)


def example_latitude_filter():
    """ 演示latitude格式判断能力
    """
    resp = client.get("/latitude", data={
        "p1": "139.9077465200"
    })
    print(resp.data)


if __name__ == "__main__":
    example_latitude_filter()
