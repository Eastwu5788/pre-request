# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2020
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-05-11 17:55'
from io import BytesIO
from flask import Flask, send_file
from werkzeug.datastructures import FileStorage
from pre_request import pre, Rule


app = Flask(__name__)
app.config["TESTING"] = True
client = app.test_client()


upload_params = {
    "params": Rule(type=FileStorage, multi=False, required=False)
}


@app.route("/upload", methods=["GET", "POST"])
@pre.catch(upload_params)
def example_upload_handler(params):
    obj = params["params"].read()
    return send_file(BytesIO(obj), mimetype="image/jpeg", as_attachment=False)


def example_upload_filter():
    """ 演示邮箱验证
    """

    with open("./static/logo.jpg", "rb") as f:
        img_io = BytesIO(f.read())

    headers = {'content-Type': 'multipart/form-data'}
    resp = client.post("/upload", headers=headers, data={
        "params": (img_io, "logo.jpg")
    })
    print(resp.data)


if __name__ == "__main__":
    example_upload_filter()
