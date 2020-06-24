Customize
===========

Response
--------------

Normally, when pre-request finds that the user input parameter does not meet the requirements, it will directly interrupt
the processing and return the discovered problem to the requester.
The default JSON type of response format provided by pre-request is as follows:

::

    {
        "respCode": 560,
        "respMsg": "Error Message",
        "result": {}
    }


In some scenarios, we need different response formats. Pre-request provides the ability to customize the response.
You need to implement a class that inherits from :class:`~pre_request.BaseResponse` to implement your own data response
processing.


::

  from flask import make_response
  from pre_request import BaseResponse

  class CusResponse(BaseResponse):

    def __call__(self, fuzzy=False, formatter=None, error=None):
        result = {
            "code": error.code,
            "rst": {}
        }
        return make_response(json.dumps(result))


::

  from pre_request import pre

  pre.add_response(CusResponse)



Formatter
------------------

If you feel that the custom response class is too complicated, we also provide the function of a custom formatting function.
The pre-request will give priority to calling your custom function to generate a response string.

::

  def custom_formatter(code, msg):
    return {
        "code": code,
        "msg": "hello",
        "sss": "tt",
    }

::

  from pre_request import pre
  pre.add_formatter(custom_formatter)


Filter
---------------

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


Store Key
----------------


By default, pre-request stores formatted input parameters in `~flask.g.params` and the `params` parameter of the current
function。 You can set the `store_key` parameter of the pre-request to change the storage key of the parameter.

::

  from pre_request import pre
  pre.store_key = "pre_params"
