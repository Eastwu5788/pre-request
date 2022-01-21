# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2020
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-04-08 09:19'
# sys
import typing as t
import json
# 3p
from flask import Flask
from pre_request import BaseResponse
from pre_request import pre, Rule, ParamsValueError


class CustomResponse(BaseResponse):

    def make_response(
            cls,
            error: "ParamsValueError",
            fuzzy: bool = False,
            formatter: t.Optional[t.Callable] = None
    ):
        result = {
            "code": 900,
            "rst": {}
        }

        from flask import make_response  # pylint: disable=import-outside-toplevel
        response = make_response(json.dumps(result))
        response.headers["Content-Type"] = "application/json; charset=utf-8"
        return response


app = Flask(__name__)
app.config["TESTING"] = True


filter_params = {
    "email": Rule(reg=r'^[A-Za-z\d]+([-_.][A-Za-z\d]+)*@([A-Za-z\d]+[-.])+[A-Za-z\d]{2,4}$')
}


@app.route("/email", methods=['get', 'post'])
@pre.catch(filter_params)
def email_resp_handler(params):
    """ 测试邮件验证
    """
    return str(params)


class TestResponse:

    def test_response(self):
        """ 测试自定义response响应
        """
        pre.add_response(CustomResponse)

        resp = app.test_client().get("/email", data={
            "email": "wudong@eastwu.cn"
        })

        assert resp.status_code == 200
        assert resp.get_data(as_text=True) == "{'email': 'wudong@eastwu.cn'}"

        resp = app.test_client().get("/email", data={
            "email": "wudong@e@astwu.cn"
        })

        assert resp.status_code == 200
        assert resp.get_data(as_text=True) == '{"code": 900, "rst": {}}'

    def test_response_none(self):
        """ 测试response恢复
        """
        pre.add_response(None)

        resp = app.test_client().get("/email", data={
            "email": "wudong@e@astwu.cn"
        })

        assert resp.status_code == 200
        assert resp.json["respMsg"] == "'email' does not match the regular expression"
