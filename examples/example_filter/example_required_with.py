# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2020
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-04-13 10:51'
""" 演示required_with协同验证过滤
"""

from flask import Flask
from pre_request import pre, Rule


app = Flask(__name__)
app.config["TESTING"] = True
client = app.test_client()


# 指定required_with=other, 当指定的其它参数填写后，要求此参数也必须填写
required_with_params = {
    "p1": Rule(required=False),
    "p2": Rule(required=False, required_with="p1", type=float)
}


@app.route("/required/with", methods=["GET", "POST"])
@pre.catch(required_with_params)
def example_required_with_handler(params):
    return str(params)


def example_required_with_filter():
    """ 演示required_with验证
    """
    resp = client.get("/required/with", data={
        "p1": "H",
        # "p2": 13
    })
    print(resp.data)


if __name__ == "__main__":
    example_required_with_filter()
