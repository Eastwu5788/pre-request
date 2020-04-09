# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2020
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-04-09 14:43'
# 3p
from flask import Flask
from pre_request import pre, Rule


def custom_formatter(code, msg):
    """ 自定义结果格式化函数

    :param code: 响应码
    :param msg: 响应消息
    """
    return {
        "code": code,
        "msg": "hello",
        "sss": "tt",
    }


app = Flask(__name__)
app.config["TESTING"] = True


filter_params = {
    "email": Rule(email=True)
}


@app.route("/email", methods=['get', 'post'])
@pre.catch(filter_params)
def email_resp_handler(params):
    """ 测试邮件验证
    """
    return str(params)


if __name__ == "__main__":
    pre.add_formatter(custom_formatter)

    resp = app.test_client().get("/email", data={
        "email": "wudong@@eastwu.cn"
    })

    print(resp.get_data(as_text=True))
