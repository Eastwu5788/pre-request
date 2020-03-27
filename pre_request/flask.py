# -*- coding: utf-8 -*-
from functools import wraps
from inspect import isfunction

from pre_request import plugins
from .exception import ParamsValueError
from .response import get_response_with_error
from .config import RequestTypeEnum


def filter_params(rules=None, **options):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 过滤规则判断
            if not options and not rules:
                return func(*args, **kwargs)

            # 如果设置了get或者post方法的过滤方式，则优先处理
            from flask import request  # pylint: disable=no-name-in-module
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
            row_params = getattr(request, "json", None)

            for key, value in param_rules.items():
                try:
                    param = request.values.get(key, default=None)
                    if not param and row_params and isinstance(row_params, dict):
                        param = row_params.get(key, None)

                    for filter_class in plugins.__all__:
                        param = getattr(plugins, filter_class)(key, param, value)()

                    # 处理用户自定义回调
                    if value.callback is not None and isfunction(value.callback):
                        param = value.callback(param)

                    result[value.key_map or key] = param
                except ParamsValueError as error:
                    return get_response_with_error(request, error, options.get("response"), RequestTypeEnum.Flask)

            kwargs = dict({"params": result}, **kwargs)

            return func(*args, **kwargs)
        return wrapper
    return decorator


def all_params():
    """此装饰器用于获取请求的所有参数，不管是GET还是POST"""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            from flask import request  # pylint: disable=no-name-in-module

            # 获取GET请求参数
            param = request.args.to_dict()
            # 获取POST参数
            param = dict(param, **request.form.to_dict())

            # 获取json请求
            json_params = getattr(request, "json", None)
            if json_params is not None:
                if isinstance(json_params, dict):
                    param = dict(param, **json_params)
                else:
                    param = dict(param, **{"json": json_params})

            # 将获取的参数返回给函数
            kwargs = dict({"params": param}, **kwargs)

            return func(*args, **kwargs)
        return wrapper
    return decorator
