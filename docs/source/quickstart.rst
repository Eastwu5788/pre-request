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


Rule 规则介绍
--------------

:class:`~pre_request.Rule` 类是用来定义请求参数规则的类，目前支持以下规则

.. code-block:: python

    # 字段目标数据类型
    self.direct_type = kwargs.get("type", str)
    # 不进行过滤，仅把参数加到结果集中
    self.skip = kwargs.get("skip", False)

    # 当前字段是否是必填项
    self.required = kwargs.get("required", True)
    self.required_with = kwargs.get("required_with", None)

    # 当前字段默认值，如果不允许为空，则次字段无意义
    self.default = kwargs.get("default", None)
    # 去除前后的空格
    self.trim = kwargs.get("trim", False)

    # 字段枚举值设置
    self.enum = kwargs.get("enum", list())

    # 正则表达式
    self.reg = kwargs.get("reg", None)
    # Email判断
    self.email = kwargs.get("email", False)
    # 手机号判断
    self.mobile = kwargs.get("mobile", False)

    # 判断字符串中包含某个子串
    self.contains = kwargs.get("contains", list())
    # 判断字符串包含任意子串
    self.contains_any = kwargs.get("contains_any", list())
    # 判断字符串中禁止包括某个子串
    self.excludes = kwargs.get("excludes", list())
    # 判断字符串开头
    self.startswith = kwargs.get("startswith", None)
    # 判断字符串结尾
    self.endswith = kwargs.get("endswith", None)
    # 字符串小写
    self.lower = kwargs.get("lower", False)
    # 字符串大写
    self.upper = kwargs.get("upper", False)

    # 判断入参是否为ipv4/ipv6
    self.ipv4 = kwargs.get("ipv4", False)
    self.ipv6 = kwargs.get("ipv6", False)
    self.mac = kwargs.get("mac", False)

    # 判断入参是否为地理坐标 经度/维度
    self.latitude = kwargs.get("latitude", False)
    self.longitude = kwargs.get("longitude", False)

    # 跨字段验证
    self.eq_key = kwargs.get("eq_key", None)
    self.neq_key = kwargs.get("neq_key", None)
    self.gt_key = kwargs.get("gt_key", None)
    self.gte_key = kwargs.get("gte_key", None)
    self.lt_key = kwargs.get("lt_key", None)
    self.lte_key = kwargs.get("lte_key", None)

    # 等于/不等于
    self.eq = kwargs.get("eq", None)
    self.neq = kwargs.get("neq", None)

    # 范围限定 direct_type 为数字时限定数字大小，为字符串时限定字符串长度
    self.gt = kwargs.get("gt", None)
    self.gte = kwargs.get("gte", None)
    self.lt = kwargs.get("lt", None)
    self.lte = kwargs.get("lte", None)

    # key映射
    self.key_map = kwargs.get("key_map", None)

    # 是否需要进行json解析
    self.json_load = kwargs.get("json", False)

    # 自定义处理callback, 在所有的filter处理完成后，通过callback回调给用户进行自定义处理
    self.callback = kwargs.get("callback", None)
