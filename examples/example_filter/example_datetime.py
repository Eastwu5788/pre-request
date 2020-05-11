# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2020
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-05-06 09:21'
# sys
from datetime import datetime
# 3p
from flask import Flask
# project
from pre_request import pre, Rule


app = Flask(__name__)
app.config["TESTING"] = True
client = app.test_client()


# 指定datetime=True，此时框架会自动判断用户入参是否符合特定的日期格式
datetime_params = {
    "birthday": Rule(type=datetime),
    "happyDay": Rule(type=datetime, eq_key="birthday"),
    "nationalDay": Rule(type=datetime, fmt="%Y-%m-%d"),
    "publishDate": Rule(type=datetime, fmt="%Y-%m-%d", gte=datetime(2019, 11, 11), lte=datetime(2019, 12, 12))
}


@app.route("/datetime", methods=["GET", "POST"])
@pre.catch(datetime_params)
def example_datetime_handler(params):
    return str(params)


def example_datetime_filter():
    """ 演示日期验证
    """
    resp = client.get("/datetime", data={
        "birthday": "2019-01-01 11:12:13",
        "nationalDay": "1949-10-01",
        "publishDate": "2019-11-18",
        "happyDay": "2019-01-01 11:12:13"
    })
    print(resp.data)


if __name__ == "__main__":
    example_datetime_filter()
