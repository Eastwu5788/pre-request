# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2020
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-05-12 10:03'
from flask import Flask
from pre_request import pre, Rule


app = Flask(__name__)
app.config["TESTING"] = True
client = app.test_client()


multi_params = {
    "p1": Rule(type=int, split=",", multi=False, required=False, default=None)
}


@app.route("/multi", methods=["GET", "POST"])
@pre.catch(multi_params)
def example_multi_handler(params):
    return str(params)


def example_multi_filter():
    """ 演示手机号验证
    """
    resp = client.get("/multi", data={
        "p1": "1, 2, 3"
    })
    print(resp.data)


if __name__ == "__main__":
    example_multi_filter()
