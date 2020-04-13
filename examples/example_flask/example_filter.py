# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2020
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-04-09 14:58'
# 3p
from flask import Flask
from pre_request import pre, Rule
from pre_request import BaseFilter
from pre_request import ParamsValueError


class CustomFilter(BaseFilter):

    def fmt_error_message(self, code):
        if code == 10086:
            return "对不起，这里是中国电信"

    def __call__(self, *args, **kwargs):
        """ 自定义过滤器时需要实现的主要功能
        """
        super(CustomFilter, self).__call__()

        if self.rule.direct_type == int and self.key == "number" and self.value != 10086:
            raise ParamsValueError(code=10086, filter=self)

        return self.value + 1


# 将自定义过滤器添加进去
pre.add_filter(CustomFilter, index=4)

app = Flask(__name__)
app.config["TESTING"] = True


filter_params = {
    "number": Rule(direct_type=int, required=True)
}


@app.route("/number", methods=['get', 'post'])
@pre.catch(filter_params)
def custom_filter_handler(params):
    """ 测试自定义过滤器验证
    """
    return str(params)


if __name__ == "__main__":

    resp = app.test_client().get("/number", data={
        "number": "10086"
    })

    print(resp.get_data(as_text=True))

    pre.remove_filter(CustomFilter)
