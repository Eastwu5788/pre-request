# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2020
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-04-13 10:51'
""" 演示skip忽略请求参数功能，pre-request仅尝试将key和value添加到params参数字典中
"""

from flask import Flask
from pre_request import pre, Rule


app = Flask(__name__)
app.config["TESTING"] = True
client = app.test_client()


# 指定skip=True, pre-request将不应用任何规则，仅将数据添加到结果字典中
skip_params = {
    "params": Rule(skip=True, type=float, default=1, required=False)
}


@app.route("/skip", methods=["GET", "POST"])
@pre.catch(skip_params)
def example_skip_handler(params):
    return str(params)


def example_skip_filter():
    """ 演示skip验证
    """
    resp = client.get("/skip", data={
        "params": 123
    })
    print(resp.data)


if __name__ == "__main__":
    example_skip_filter()
