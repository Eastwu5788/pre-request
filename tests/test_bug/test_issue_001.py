# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2020
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-08-07 10:10'
import json
from flask import make_response, Flask
from pre_request import pre, Rule


app = Flask(__name__)
app.config["TESTING"] = True
client = app.test_client()


def json_resp(result):
    result = json.dumps(result)
    resp = make_response(result)
    resp.headers['Content-Type'] = 'application/json'
    return resp


args = {
    "userId": Rule(type=str, gte=1, lte=20, required=False, multi=True, dest="user_id_s")
}


@app.route("/bug", methods=["GET", "POST"])
@pre.catch(args)
def structure_handler(params):
    return json_resp(params)


class TestStructure:

    def test_structure_smoke(self):
        """ 测试带数据结构的参数处理
        """
        resp = app.test_client().post("/bug", json={})
        assert resp.json == {"user_id_s": []}
