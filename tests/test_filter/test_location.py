# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2021
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2022/1/19 1:43 下午'
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


# latitude，框架将验证入参是否符合地理纬度规则
args = {
    "latitude": Rule(latitude=True),
    "longitude": Rule(longitude=True)
}


@app.route("/location", methods=["GET", "POST"])
@pre.catch(args)
def handler(params):
    return json_resp(params)


class TestLocation:

    def test_location_smoke(self):
        """ 测试地理纬度
        """
        resp = app.test_client().get("/location", data={
            "longitude": "+40.70680040974271",
            "latitude": "-74.01125485098078",
        })

        assert resp.json == {'latitude': '-74.01125485098078', 'longitude': '+40.70680040974271'}

    def test_longitude_invalid(self):
        """ 测试地理纬度
        """
        resp = app.test_client().get("/location", data={
            "longitude": "180.70680040974271",
            "latitude": "-74.01125485098078",
        })

        assert resp.json["respMsg"] == "'longitude' can't be converted to longitude"

    def test_latitude_invalid(self):
        """ 测试地理纬度
        """
        resp = app.test_client().get("/location", data={
            "longitude": "40.70680040974271",
            "latitude": "-90.01125485098078",
        })

        assert resp.json["respMsg"] == "'latitude' can't be converted to latitude"
