# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2020
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-04-26 09:19'
from flask import Flask
from pre_request import pre, Rule

app = Flask(__name__)
app.config["TESTING"] = True
client = app.test_client()


args = {
    "userInfo": {
        "userId": Rule(type=int, required=False),
        "userName": Rule(type=str, required=False, default=""),
        "socialInfo": {
            "gender": Rule(type=int, enum=[1, 2], default=1),
            "age": Rule(type=int, gte=18, lt=80),
            "school": Rule(type=str, required=False, default=""),
        }
    },
    "otherUserId": Rule(type=int, required=False, required_with="userInfo.userId")
}


@app.route("/structure", methods=["GET", "POST"])
@pre.catch(args)
def structure_handler(params):
    return str(params)


if __name__ == "__main__":
    resp = app.test_client().post("/structure", data={
        "userId": "13",
        "userName": "张三",
        "gender": 1,
        "age": 18,
        "school": "Dog",
        "otherUserId": 12,
    })

    print(resp.get_data(as_text=True))
    print(resp.json)
