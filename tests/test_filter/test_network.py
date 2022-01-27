# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2021
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2022/1/24 9:40 上午'
import json
from flask import make_response, Flask
from pre_request import pre, Rule


app = Flask(__name__)
app.config["TESTING"] = True


def json_resp(result):
    result = json.dumps(result)
    resp = make_response(result)
    resp.headers['Content-Type'] = 'application/json'
    return resp


args = {
    "p1": Rule(type=str, url_decode=True, encoding="GB2312"),
    "p2": Rule(type=str, url_encode=True, multi=True)
}


@app.route("/network", methods=["GET", "POST"])
@pre.catch(args)
def network_handler(params):
    return json_resp(params)


class TestNetwork:

    def test_network_smoke(self):
        resp = app.test_client().post("/network", json={
            "p1": "https%3A%2F%2Fwww.test.com%2Fsd%3Fid%3D%B9%FE",
            "p2": ["https://www.test.com/sd?id=哈"]
        })

        assert resp.json == {
            "p1": "https://www.test.com/sd?id=哈",
            "p2": ["https%3A%2F%2Fwww.test.com%2Fsd%3Fid%3D%E5%93%88"]
        }
