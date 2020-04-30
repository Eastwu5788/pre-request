# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2020
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-04-28 10:12'
from flask import g, Flask
from pre_request import pre, Rule


app = Flask(__name__)
app.config["TESTING"] = True
client = app.test_client()


# 指定email=True，此时框架会自动判断用户入参是否符合email正则
args = {
    "params": Rule(email=True)
}


pre.store_key = "test_params"


@app.route("/email", methods=["GET", "POST"])
@pre.catch(args)
def example_storage_handler(test_params):
    print(g.test_params)
    print(test_params)
    return str(test_params)


if __name__ == "__main__":
    resp = client.get("/email", data={
        "params": "wudong@eastwu.cn"
    })
    print(resp.data)
