# -*- coding: utf-8 -*-

from functools import wraps
from inspect import isfunction

from .filter_error import ParamsValueError
from .filter_config import FILTER_LIST
from .filter_response import get_response_with_error
from .filter_config import RequestTypeEnum


def filter_params(rules=None, **options):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 过滤规则判断
            if not options and not rules:
                return func(*args, **kwargs)

            # tornado.request_handler
            handler = args[0]

            # 如果设置了get或者post方法的过滤方式，则优先处理
            if handler.request.method == "GET":
                param_rules = options.get("get")
            else:
                param_rules = options.get("post")

            # 如果未处理get或者post，则使用rules
            if not param_rules:
                if rules:
                    param_rules = rules
                else:
                    return func(*args, **kwargs)

            result = dict()
            for key, rule in param_rules.items():
                try:
                    param = handler.get_argument(key, default=None)
                    # 依次执行过滤器
                    for filter_class in FILTER_LIST:
                        param = filter_class(key, param, rule)()

                    # 处理用户自定义回调
                    if rule.callback is not None and isfunction(rule.callback):
                        param = rule.callback(param)

                    # 存储过滤后的值
                    result[rule.key_map or key] = param
                except ParamsValueError as error:
                    return get_response_with_error(handler, error, options.get("response"), RequestTypeEnum.Tornado)

            kwargs = dict({"params": result}, **kwargs)

            return func(*args, **kwargs)
        return wrapper
    return decorator

