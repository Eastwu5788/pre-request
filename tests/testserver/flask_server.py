# -*- coding: utf-8 -*-
# (C) Wu Dong, 2018
# All rights reserved
__author__ = 'Wu Dong <wudong@eastwu.cn>'
__time__ = '2018/9/6 11:21'
from flask import Flask
from flask.views import MethodView, View

from pre_request.flask import filter_params
from pre_request.filter_rules import Rule, Length, Range


app = Flask(__name__)
app.debug = True

field = {
    "age": Rule(direct_type=int, enum=[1, 2]),
    "name": Rule(length=Length(6, 12)),
    "email": Rule(email=True),
    "mobile": Rule(mobile=True),
    "empty": Rule(allow_empty=True, default="sssss_empty")
}

get_field = {
    "year": Rule(direct_type=int, enum=[1920, 1922]),
    "string": Rule(length=Length(6, 12)),
    "range": Rule(range=Range('ab', 'zg')),
    "email": Rule(email=True),
    "mobile": Rule(mobile=True),
    "reg": Rule(reg=r'^h\w{3,5}o$'),
    "trim": Rule(trim=True)
}

post_field = {
    "year": Rule(direct_type=int),
    "empty": Rule(allow_empty=True, default="asdf"),
    "range": Rule(direct_type=int, range=Range(10, 30)),
    "reg": Rule(reg=r'^m\d+m$')
}


@app.route("/test", methods=['get', 'post'])
@filter_params(field)
def test_handler(params=None):
    return str(params)


@app.route("/get", methods=['get'])
@filter_params(get=get_field)
def get_handler(params=None):
    return str(params)


@app.route("/post", methods=['post'])
@filter_params(post=post_field)
def post_handler(params=None):
    return str(params)


@app.route("/all", methods=['get', 'post'])
@filter_params(get=get_field, post=post_field)
def all_handler(params=None):
    return str(params)


# 方法视图
class GetView(MethodView):

    @filter_params(get=get_field)
    def get(self, params=None):
        return str(params)

    @filter_params(post=post_field, response='html')
    def post(self, params=None):
        return str(params)


# 标准视图demo
class BaseView(View):

    @filter_params(get=get_field, post=post_field, response='html')
    def dispatch_request(self, params=None):
        return str(params)


app.add_url_rule('/getview', view_func=GetView.as_view('getview'))
app.add_url_rule('/baseview', view_func=BaseView.as_view('baseview'))


if __name__ == "__main__":
    app.run()

