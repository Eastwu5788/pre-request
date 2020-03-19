# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2020
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-03-19 11:14'
""" 演示 pre-request 框架如何使用参数字段映射
"""
from flask import Flask
from pre_request import filter_params, Rule


app = Flask(__name__)
app.config["TESTING"] = True
client = app.test_client()


# 指定key_map，框架会将参数变更为 key_map 指定的key
map_params = {
    "params": Rule(key_map="key")
}


@app.route("/map", methods=["GET", "POST"])
@filter_params(map_params)
def example_map_handler(params):
    return str(params)


def example_map_filter():
    """ 演示邮箱验证
    """
    resp = client.get("/map", data={
        "params": "wudong@eastwu.cn"
    })
    print(resp.data)


if __name__ == "__main__":
    example_map_filter()
