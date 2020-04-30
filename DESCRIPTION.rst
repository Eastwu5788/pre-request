Pre-request
===========

.. image:: https://raw.githubusercontent.com/Eastwu5788/pre-request/master/docs/static/logo.jpg
   :align: center

..  image:: https://www.travis-ci.org/Eastwu5788/pre-request.svg?branch=master
    :target: https://www.travis-ci.org/Eastwu5788/pre-request

..  image:: https://coveralls.io/repos/github/Eastwu5788/pre-request/badge.svg?branch=master
    :target: https://coveralls.io/github/Eastwu5788/pre-request?branch=master

..  image:: https://img.shields.io/pypi/l/pre-request?color=brightgreen
    :alt: PyPI - License

..  image:: https://readthedocs.org/projects/pre-request/badge/?version=master
    :target: https://pre-request.readthedocs.io/en/master/?badge=master
    :alt: Documentation Status

..  image:: https://img.shields.io/pypi/v/pre-request?color=brightgreen
    :target: https://pypi.org/project/pre-request/
    :alt: PyPI

.. image:: https://badges.gitter.im/pre-request/community.svg?color=brightgreen
   :target: https://gitter.im/pre-request/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge
   :alt: Im


欢迎您使用pre-request框架，pre-request致力于简化请求参数验证工作。为Flask的
网络请求参数验证提供了解决方案。

pre-request提供了非常方便的使用的方法，也提供了灵活的扩展接口方便您实现自定义的
业务逻辑。

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

   from pre_request import pre
   from pre_request import Rule

   app = Flask(__name__)

   args = {
      "userId": Rule(type=int, required=True)
   }

   @app.route("/")
   @pre.catch(args)
   def hello_world(params):
      from flask import g
      return params == g.params

上面的代码中发生了什么呢？

1. 首先我们从 `pre-request` 库中引入全局 `pre` 对象，使用该对象来过滤用户参数
2. 我们定义了一个请求参数 `userId` 并规定该参数的目标类型为 `int` ，并且不允许为空
3. 使用 `@pre.catch(req_params)` 将参数规则赋值给装饰器，并装饰处理函数
4. 格式化后的参数置于 `~flask.g` 中，同时尝试将格式化后的参数置于原函数的 `params` 参数中。


Links
------------
* Documentaion: https://pre-request.readthedocs.io/en/master/index.html
* Release: https://pypi.org/project/pre-request/
* Code: https://github.com/Eastwu5788/pre-request
* Issue tracker: https://github.com/Eastwu5788/pre-request/issues
* Test status: https://coveralls.io/github/Eastwu5788/pre-request
