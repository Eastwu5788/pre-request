# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2020
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-04-08 09:50'
# 3p
from flask import Flask
from pre_request import pre, Rule


def custom_formatter(error):
    """ 自定义结果格式化函数
    """
    return {
        "code": 411,
        "msg": "hello",
        "sss": "tt",
    }


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


class TestFormatter:

    def test_formatter(self):
        """ 测试自定义formatter
        """
        pre.add_formatter(custom_formatter)

        resp = app.test_client().get("/email", data={
            "email": "wudong@eastwu.cn"
        })

        assert resp.status_code == 200
        assert resp.get_data(as_text=True) == "{'email': 'wudong@eastwu.cn'}"

        resp = app.test_client().get("/email", data={
            "email": "wudong@e@astwu.cn"
        })

        assert resp.status_code == 200
        assert resp.get_data(as_text=True) == '{"code": 411, "msg": "hello", "sss": "tt"}'

    def test_resp_error(self):
        """ 测试重置response时报错问题
        """
        pre.add_formatter(None)

    def test_response_none(self):
        """ 测试response恢复
        """
        resp = app.test_client().get("/email", data={
            "email": "wudong@e@astwu.cn"
        })

        assert resp.status_code == 200
        assert resp.json["respMsg"] == "'email' does not match the regular expression"
