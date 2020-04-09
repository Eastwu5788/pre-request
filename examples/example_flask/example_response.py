# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2020
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-04-09 14:39'
""" 演示自定义响应类
"""
# sys
import json
# 3p
from flask import Flask
from pre_request import BaseResponse
from pre_request import pre, Rule


class CustomResponse(BaseResponse):

    def __call__(self, formatter=None, error=None):
        """
        :type error: 错误
        :return:
        """
        result = {
            "code": error.code,
            "rst": {}
        }

        from flask import make_response  # pylint: disable=import-outside-toplevel
        response = make_response(json.dumps(result))
        response.headers["Content-Type"] = "application/json; charset=utf-8"
        return response


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
    pre.add_response(CustomResponse)

    resp = app.test_client().get("/email", data={
        "email": "wudong@@eastwu.cn"
    })

    print(resp.get_data(as_text=True))
