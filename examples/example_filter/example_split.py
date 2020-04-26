# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2020
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-04-26 10:49'
from flask import Flask
from pre_request import pre, Rule


app = Flask(__name__)
app.config["TESTING"] = True
client = app.test_client()


# 指定split=","，pre-request会尝试将参数按指定字符串分割
split_params = {
    "p1": Rule(type=str, split=",", trim=True, upper=True),
    "p2": Rule(split=",", trim=True, lower=True),
    "p3": Rule(type=int, split=",", lte=5)
}


@app.route("/split", methods=["GET", "POST"])
@pre.catch(split_params)
def example_split_handler(params):
    return str(params)


def example_split_filter():
    """ 演示skip验证
    """
    resp = client.get("/split", data={
        "p1": "aBc, 394,394  ",
        "p2": "ABC",
        "p3": "4, 2, 3"
    })
    print(resp.data)
    print(resp.json)


if __name__ == "__main__":
    example_split_filter()
