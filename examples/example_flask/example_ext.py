# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2020
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-05-12 17:27'
from flask import g, Flask
from pre_request import pre, Rule


app = Flask(__name__)
app.config["TESTING"] = True

app.config["PRE_FUZZY"] = True
app.config["PRE_STORE_KEY"] = "pp"


client = app.test_client()


# 指定email=True，此时框架会自动判断用户入参是否符合email正则
email_params = {
    "params": Rule(email=True)
}


@app.route("/email", methods=["GET", "POST"])
@pre.catch(email_params)
def example_email_handler():
    return str(g.pp)


def example_email_filter():
    """ 演示邮箱验证
    """
    pre.init_app(app=app)
    resp = client.get("/email", data={
        "params": "wudon@g@eastwu.cn"
    })
    print(resp.data)


if __name__ == "__main__":
    example_email_filter()
