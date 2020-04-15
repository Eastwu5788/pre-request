# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2020
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-04-13 10:54'
""" 演示 pre-request 框架验证不同参数联动限制禁止相等
"""
import json
from flask import Flask
from pre_request import pre, Rule


app = Flask(__name__)
app.config["TESTING"] = True
client = app.test_client()


# 指定gt_key, 禁止两个参数相等
gt_key_params = {
    "p1": Rule(direct_type=int),
    "p2": Rule(direct_type=int, gt_key="p1")
}


@app.route("/gt/key", methods=["GET", "POST"])
@pre.catch(gt_key_params)
def example_gt_key_handler(params):
    return str(params)


def example_gt_key_filter():
    """ 演示gt_key包含函数
    """
    resp = client.get("/gt/key", data={
        "p1": 15,
        "p2": 13
    })
    print(json.loads(resp.data))


if __name__ == "__main__":
    example_gt_key_filter()
