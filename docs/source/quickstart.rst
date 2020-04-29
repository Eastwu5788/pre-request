快速开始
===============

本篇文档将向您介绍pre-request的详细使用方式，帮助您尽快将pre-request应用于您的项目。

Minimal Usage
----------------

pre-request最简单的使用方式

.. code-block:: python

   from flask import Flask

   from pre_request import pre
   from pre_request import Rule

   app = Flask(__name__)

   req_params = {
      "userId": Rule(type=int, required=True)
   }

   @app.route("/")
   @pre.catch(req_params)
   def hello_world(params):
      return str(params)


上面的代码中发生了什么呢？

1. 首先我们从 `pre-request` 库中引入全局 `pre` 对象，使用该对象来过滤用户参数
2. 我们定义了一个请求参数 `userId` 并规定该参数的目标类型为 `int` ，并且不允许为空
3. 使用 `@pre.catch(req_params)` 将参数规则赋值给装饰器，并装饰处理函数
4. 格式化后的参数置于 :class:`~flask.g` 中，同时尝试将格式化后的参数置于原函数的 `params` 参数中。


`pre` 单例介绍
---------------

pre-request 提供了一个全局单例 `pre` 对象，我们可以通过操作 `pre` 来修改pre-request的运行参数。

-  `pre.fuzzy` 指示pre-request是否对参数验证错误原因进行模糊化处理。防止暴露过多信息
-  `pre.sore_key` 自定义pre-request解析完成的参数的存储key
-  `pre.content_type` 设置pre-request的错误响应格式，目前支持 `application/json` 和 `text/html`


`@pre.catch` 装饰器介绍
-------------------------

pre-request的过滤能力主要是通过`@pre.catch`装饰器来实现的

我们可以使用 `@pre.catch` 过滤指定method的请求参数, 也可以指定针对特定请求 `method` 进行过滤

.. code-block:: python

    @app.route("/get", methods=['get'])
    @pre.catch(get=req_params)
    def get_handler(params):
        return str(params)

    @app.route("/post", methods=['post'])
    @pre.catch(post=req_params)
    def get_handler(params):
        return str(params)

当然我们也为使用不同请求方式解析不同参数的情况提供了支持

.. code-block:: python

    # 同时设置get和post的过滤参数
    @app.route("/all", methods=['get', 'post'])
    @pre.catch(get=get_field, post=post_field)
    def all_handler(params):
        return str(params)
