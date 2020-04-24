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
2. 提供跨字段的参数验证能力，实现两个字段关联验证
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
      return params == g.params

上面的代码中发生了什么呢？

1. 首先我们从 `pre-request` 库中引入全局 `pre` 对象，使用该对象来过滤用户参数
2. 我们定义了一个请求参数 `userId` 并规定该参数的目标类型为 `int` ，并且不允许为空
3. 使用 `@pre.catch(req_params)` 将参数规则赋值给装饰器，并装饰处理函数
4. 格式化后的参数置于 `~flask.g` 中，同时尝试将格式化后的参数置于原函数的 `params` 参数中。


Rule 规则概览
----------------

::

    # 参数来源位置
    self.location = kwargs.get("location", None)
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
    # 是否是文件路径
    # self.file = kwargs.get("file", False)

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
    self.key_map = kwargs.get("dest", None)

    # 是否需要进行json解析
    self.json_load = kwargs.get("json", False)

    # 自定义处理callback, 在所有的filter处理完成后，通过callback回调给用户进行自定义处理
    self.callback = kwargs.get("callback", None)


贡献代码
----------

非常欢迎大家能够贡献自己的代码到项目中来，具体的提交流程请参考 `contributing`_.

.. _contributing: https://github.com/Eastwu5788/pre-request/blob/master/CONTRIBUTING.rst


Links
------------
* Documentaion: https://pre-request.readthedocs.io/en/master/index.html
* Release: https://pypi.org/project/pre-request/
* Code: https://github.com/Eastwu5788/pre-request
* Issue tracker: https://github.com/Eastwu5788/pre-request/issues
* Test status: https://coveralls.io/github/Eastwu5788/pre-request
