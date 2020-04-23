# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2020
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-04-23 10:22'
from flask import g, Flask
from pre_request import pre, Rule


app = Flask(__name__)
app.config["TESTING"] = True
client = app.test_client()


# 指定email=True，此时框架会自动判断用户入参是否符合email正则
params = {
    "p1": Rule(type=int, location="args"),
    "p2": Rule(type=int, location="form"),
    "p3": Rule(type=int, location="values"),
    "p4": Rule(type=int, location="headers"),
    "p5": Rule(type=int, location="cookies"),
}


@app.route("/email", methods=["GET", "POST"])
@pre.catch(params)
def example_email_handler():
    return str(g.params)


json = {
    "p6": Rule(type=int, location="json")
}


@app.route("/json", methods=["GET", "POST"])
@pre.catch(json)
def example_json_handler():
    return str(g.params)


multi = {
    "p7": Rule(type=int, location=["cookies", "args", "form", "headers"])
}


@app.route("/multi", methods=["GET", "POST"])
@pre.catch(multi)
def example_multi_handler():
    return str(g.params)


def example_filter():
    """ 演示邮箱验证
    """
    client.set_cookie("localhost", "p5", "5")
    resp = client.get("/email?p1=1", data={
        "p2": 2,
        "p3": 3,
    }, headers={
        "p4": "4"
    })
    print(resp.data)

    resp = client.get("/json", json={
        "p6": 6
    })
    print(resp.data)

    client.set_cookie("localhost", "p7", "7777")
    resp = client.get("/multi?p7=7", data={
        "p7": 77
    }, headers={
        "p7": 777
    })
    print(resp.data)


if __name__ == "__main__":
    example_filter()
