# -*- coding: utf-8 -*-

from functools import wraps
from .filter_config import FILTER_LIST
from .filter_error import ParamsValueError
from .filter_response import get_response_with_error
from .filter_config import RequestTypeEnum


def filter_params(rules=None, **options):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 过滤规则判断
            if not options and not rules:
                return func(*args, **kwargs)

            # 如果设置了get或者post方法的过滤方式，则优先处理
            from flask import request
            if request.method == "GET":
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
            for key, value in param_rules.items():
                try:
                    param = request.values.get(key, default=None)
                    for filter_class in FILTER_LIST:
                        param = filter_class(key, param, value)()
                    result[key] = param
                except ParamsValueError as error:
                    return get_response_with_error(request, error, options.get("response"), RequestTypeEnum.Flask)

            kwargs = dict({"params": result}, **kwargs)

            return func(*args, **kwargs)
        return wrapper
    return decorator

