.. raw:: html

    <p align="center">
        <a href="#readme">
            <img alt="Pre-request logo" src="https://raw.githubusercontent.com/Eastwu5788/pre-request/master/docs/static/logo.jpg">
        </a>
    </p>
    <p align="center">
        <a href="https://www.travis-ci.org/Eastwu5788/pre-request"><img alt="Travis" src="https://www.travis-ci.org/Eastwu5788/pre-request.svg?branch=master"></a>
        <a href="https://coveralls.io/github/Eastwu5788/pre-request?branch=master"><img alt="Coveralls" src="https://coveralls.io/repos/github/Eastwu5788/pre-request/badge.svg?branch=master"></a>
        <a href="https://github.com/Eastwu5788/pre-request/blob/master/LICENSE"><img alt="License" src="https://img.shields.io/pypi/l/pre-request?color=brightgreen"></a>
        <a href="https://pre-request.readthedocs.io/en/master/"><img alt="Docs" src="https://readthedocs.org/projects/pre-request/badge/?version=master"></a>
        <a href="https://pypi.org/project/pre-request/"><img alt="PyPI" src="https://img.shields.io/pypi/v/pre-request?color=brightgreen"></a>
        <a href="https://gitter.im/pre-request/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge"><img alt="IM" src="https://badges.gitter.im/pre-request/community.svg"/></a>
    </p>


========

欢迎使用pre-request框架，pre-request致力于简化参数验证工作，目前pre-request仅支持Flask
的请求参数验证。

pre-request提供了非常方便的使用方法，也提供了灵活的扩展机制，让您可以自定义各个模块，实现您自身的复杂需求。

特点
----

1. 提供绝大部分常用的参数基础验证能力，也提供callback函数让用户自定义验证
2. 提供跨字段的、跨数据结构的参数验证能力，实现参数之间关联验证
3. 提供响应对象、格式化函数、过滤器等核心组件的自定义能力
4. 详细完善的测试用例，保证整体测试覆盖率高于90%
5. 丰富的example，演示了pre-request目前提供的所有能力

安装
----

::

    pip install pre-request


快速使用
----------------

集成pre-request到您的请求中非常简单

.. code-block:: python

   from flask import Flask

   from pre_request import pre, Rule

   app = Flask(__name__)

   args = {
      "userId": Rule(type=int, required=True)
   }

   @app.route("/")
   @pre.catch(args)
   def hello_world(params):
      from flask import g
      return str(params == g.params)

上面的代码中发生了什么呢？

1. 首先我们从 `pre-request` 库中引入全局 `pre` 对象，使用该对象来过滤用户参数
2. 我们定义了一个请求参数 `userId` 并规定该参数的目标类型为 `int` ，并且不允许为空
3. 使用 `@pre.catch(req_params)` 将参数规则赋值给装饰器，并装饰处理函数
4. 格式化后的参数置于 `~flask.g` 中，同时尝试将格式化后的参数置于原函数的 `params` 参数中。


复杂示例
--------------

我们使用一个复杂的示例来演示pre-request的魅力

.. code-block:: python

    from flask import Flask
    from pre_request import pre, Rule

    args = {
        "userFirst": {
            "userId": Rule(type=int, required=False),
            "socialInfo": {
                "gender": Rule(type=int, enum=[1, 2], default=1),
                "age": Rule(type=int, gte=18, lt=80),
                "country": Rule(required=True, deep=False)
            }
        },
        "userSecond": {
            "userId": Rule(type=int, required=False, neq_key="userFirst.userId"),
            "socialInfo": {
                "gender": Rule(type=int, enum=[1, 2], default=1, neq_key="userFirst.socialInfo.gender"),
                "age": Rule(type=int, gte=18, lt=80, required_with="userFirst.socialInfo.age"),
                "country": Rule(required=True, deep=False)
            }
        }
    }


    app = Flask(__name__)
    app.config["TESTING"] = True
    client = app.test_client()

    @app.route("/structure", methods=["GET", "POST"])
    @pre.catch(args)
    def structure_handler(params):
        return str(params)


    if __name__ == "__main__":
        resp = app.test_client().post("/structure", json={
            "userFirst": {
                "userId": "13",
                "socialInfo": {
                    "age": 20,
                }
            },
            "userSecond": {
                "userId": 14,
                "socialInfo": {
                    "age": 21
                }
            },
            "country": "CN",
            "userFirst.socialInfo.gender": 1,
            "userSecond.socialInfo.gender": 2,
        })

        print(resp.get_data(as_text=True))

贡献代码
----------

非常欢迎大家能够贡献自己的代码到项目中来，具体的提交流程请参考 `contributing`_.

.. _contributing: https://github.com/Eastwu5788/pre-request/blob/master/CONTRIBUTING.rst


相关链接
------------
* Documentaion: https://pre-request.readthedocs.io/en/master/index.html
* Release: https://pypi.org/project/pre-request/
* Code: https://github.com/Eastwu5788/pre-request
* Issue tracker: https://github.com/Eastwu5788/pre-request/issues
* Test status: https://coveralls.io/github/Eastwu5788/pre-request
