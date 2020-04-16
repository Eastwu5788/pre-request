自定义响应
===========

通常情况下，pre-request 检查用户参数发现问题时，会直接中断处理并将发现的问题返回给请求方。pre-request提供的
默认JSON响应格式如下：

::

    {
        "respCode": 560,
        "respMsg": "错误消息",
        "result": {}
    }


但是在显示场景中，每个人都需要特定的响应格式。所以pre-request提供了自定义响应的功能。您仅需要实现一个类继承自 :class:`~pre_request.BaseResponse`
即可实现您自己的数据响应。


::

  from flask import make_response
  from pre_request import BaseResponse

  class CusResponse(BaseResponse):

    def __call__(self, formatter=None, error=None):
        result = {
            "code": error.code,
            "rst": {}
        }
        return make_response(json.dumps(result))


当然，我们需要您在初始化您的项目的时候，设置一下 pre-request 使用您的自定义响应


::

  from pre_request import pre

  pre.add_response(CusResponse)



自定义格式化内容
================

如果您觉得自定义一个响应类过于复杂，我们也提供了更轻便的自定义格式化函数功能，pre-request 在尝试拼接响应内容的时候，会优先尝试调用您的
格式化函数生成响应字符串。

::

  def custom_formatter(code, msg):
    """ 自定义结果格式化函数
    """
    return {
        "code": code,
        "msg": "hello",
        "sss": "tt",
    }


我们会尝试将错误码和格式化后的错误消息传递到函数中，根据我们提供的参数，您就可以返回一个特点的内容，返回给请求方

当然，我们也同样需要您设置pre-request使用您提供的格式化函数

::

  from pre_request import pre
  pre.add_formatter(custom_formatter)


自定义过滤器
===============

pre-request 提供了丰富的过滤器插件。但是面对各式各样的业务需求，您可能也觉得pre-request无法满足您。因此pre-request
提供了自定义过滤器功能，让您可以更加自身的业务需求去扩展pre-request框架。

通常情况下，自定义的过滤器需要继承自 :class:`~pre_request.BaseFilter` 类。

::

    from pre_request import BaseFilter

    class CustomFilter(BaseFilter):

        def fmt_error_message(self, code):
            if code == 10086:
                return "对不起，这里是中国电信"

        def filter_required(self):
            """ 检查当前过滤式，是否必须要执行
            """
            return True

        def __call__(self, *args, **kwargs):
            """ 自定义过滤器时需要实现的主要功能
            """
            super(CustomFilter, self).__call__()

            if self.rule.direct_type == int and self.key == "number" and self.value != 10086:
                raise ParamsValueError(code=10086, filter=self)

            return self.value + 1

如上所示，您至少需要实现`fmt_error_message`、`filter_required` 和 `__call__` 方法。在运行您的过滤器之前，先调用
`filter_required` 方法判断当前过滤器是否需要被执行，然后再调用 `__call__` 方法运行过滤器。当发现过滤失败后，会调用
`fmt_error_message` 来通知过滤器格式化错误消息。

最后，您需要在项目初始化时将自定义过滤器安装到pre-request中

::

    from pre_request import pre

    pre.add_filter(CustomFilter)
