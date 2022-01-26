# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2020
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-05-12 10:09'
# sys
from io import BytesIO

# 3p
from flask import Flask, send_file
from werkzeug.datastructures import FileStorage

# project
from pre_request import pre, Rule


app = Flask(__name__)
app.config["TESTING"] = True


args = {
    "p1": Rule(type=FileStorage)
}


@app.route("/upload", methods=["GET", "POST"])
@pre.catch(args)
def example_upload_handler(params):
    return send_file(BytesIO(params["p1"].read()), mimetype="image/jpeg", as_attachment=False)


args2 = {
    "p1": Rule(type=FileStorage, multi=True)
}


@app.route("/upload2", methods=["GET", "POST"])
@pre.catch(args2)
def example_upload2_handler(params):
    return send_file(BytesIO(params["p1"][0].read()), mimetype="image/jpeg", as_attachment=False)


class TestUpload:

    def test_upload_smoke(self):
        with open("./tests/static/logo.jpg", "rb") as f:
            f_b = f.read()

            headers = {'content-Type': 'multipart/form-data'}
            resp = app.test_client().post("/upload", headers=headers, data={
                "p1": (BytesIO(f_b), "logo.jpg")
            })

            assert resp.data == f_b

    def test_upload2_smoke(self):
        with open("./tests/static/logo.jpg", "rb") as f:
            f_b = f.read()

            headers = {'content-Type': 'multipart/form-data'}
            resp = app.test_client().post("/upload2", headers=headers, data={
                "p1": (BytesIO(f_b), "logo.jpg")
            })

            assert resp.data == f_b

    def test_upload_560(self):
        headers = {'content-Type': 'multipart/form-data'}
        resp = app.test_client().post("/upload", headers=headers)
        assert resp.json["respMsg"] == "'p1' can't be empty"
