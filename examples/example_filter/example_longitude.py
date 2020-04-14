# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2020
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-04-13 10:54'
""" 演示 pre-request 框架验证字符串是否符合地理经度坐标
"""
from flask import Flask
from pre_request import pre, Rule


app = Flask(__name__)
app.config["TESTING"] = True
client = app.test_client()


# longitude，框架将验证入参是否符合地理纬度规则
longitude_params = {
    "p1": Rule(longitude=True)
}


@app.route("/longitude", methods=["GET", "POST"])
@pre.catch(longitude_params)
def example_longitude_handler(params):
    return str(params)


def example_longitude_filter():
    """ 演示latitude格式判断能力
    """
    resp = client.get("/longitude", data={
        "p1": "116.3860159600"
    })
    print(resp.data)


if __name__ == "__main__":
    example_longitude_filter()
