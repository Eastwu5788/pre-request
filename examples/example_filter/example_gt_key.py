# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2020
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-04-13 10:54'
""" 演示 pre-request 框架验证不同参数联动限制禁止相等
"""
import json
from datetime import datetime
from flask import Flask
from pre_request import pre, Rule


app = Flask(__name__)
app.config["TESTING"] = True
client = app.test_client()


# 指定gt_key, 禁止两个参数相等
gt_key_params = {
    "p1": Rule(type=datetime, dest="P1"),
    "p2": Rule(type=datetime, gt_key="P1", dest="P2")
}


@app.route("/gt/key", methods=["GET", "POST"])
@pre.catch(gt_key_params)
def example_gt_key_handler(params):
    return str(params)


def example_gt_key_filter():
    """ 演示gt_key包含函数
    """
    resp = client.get("/gt/key", data={
        "p1": "2020-01-01 12:00:00",
        "p2": "2019-12-12 12:00:00"
    })
    print(json.loads(resp.data))


if __name__ == "__main__":
    example_gt_key_filter()
