# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2020
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-04-01 09:47'
# sys
from functools import wraps
from inspect import isfunction

# object
from .exception import ParamsValueError
from .filters.base import BaseFilter
from .response import JSONResponse, HTMLResponse, BaseResponse
from .rules import Rule
from . import filters


class PreRequest:
    """ An object to dispatch filters to handler request params
    """

    def __init__(self, content_type=None):
        self.filters = filters.__all__
        self.content_type = content_type or "application/json"
        self.response = None
        self.formatter = None

    def add_response(self, resp):
        """ Add custom response class

        :param resp: response class which is subclass of BaseResponse
        """
        if resp and not issubclass(resp, BaseResponse):
            raise TypeError("custom response must be subclass of `pre_request.BaseResponse`")

        self.response = resp

    def add_formatter(self, fmt):
        """ Add custom format function for generate response content

        :param fmt: format function
        """
        if fmt and not isfunction(fmt):
            raise TypeError("custom format function must be a type of function")

        if fmt and fmt.__code__.co_argcount < 2:
            raise TypeError("custom format function requires at least 2 arguments")

        self.formatter = fmt

    def add_filter(self, cus_filter, index=None):
        """ Add custom filter class to extend pre-request

        :param cus_filter: custom filter class
        :param index: filter position
        """
        if cus_filter and not issubclass(cus_filter, BaseFilter):
            raise TypeError("custom filter must be subclass of `BaseFilter`")

        if index is not None and not isinstance(index, int):
            raise TypeError("index params must be type of Int")

        if index is not None:
            self.filters.insert(index, cus_filter)
        else:
            self.filters.append(cus_filter)

    def remove_filter(self, cus_filter=None, index=None):
        """ 移除指定过滤器

        :param cus_filter: 过滤器名称
        :param index: 过滤器位置
        """
        if cus_filter and (isinstance(cus_filter, str) or issubclass(cus_filter, BaseFilter)):
            self.filters.remove(cus_filter)

        if index is not None and isinstance(index, int) and 0 <= index < len(self.filters):
            self.filters.pop(index)

    @staticmethod
    def _f_params(key, default=None):
        """ Query request params from flask request object

        :param key: params key
        """
        from flask import request  # pylint: disable=import-outside-toplevel

        # query params from simple method
        value = request.values.get(key, default)
        if value is not None:
            return value

        # query params from json request
        json_value = getattr(request, "json")
        if json_value and isinstance(json_value, dict):
            return json_value.get(key, default)

        return default

    def catch(self, rule=None, **options):
        """ Catch request params
        """
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                kwargs["params"] = rst = dict()

                # ignore with empty rule
                if not rule and not options:
                    return func(*args, **kwargs)

                # query rules with special method
                from flask import request  # pylint: disable=import-outside-toplevel
                rules = options.get(request.method) or options.get(request.method.lower())

                # common rule
                if rules is None and rule is not None:
                    rules = rule

                # ignore catch with empty rules
                if not rules:
                    raise ValueError("request method '%s' with invalid filter rule" % request.method)

                for k, r in rules.items():
                    try:
                        value = self._f_params(k)

                        # invalid rule
                        if not isinstance(r, Rule):
                            rst[k] = value
                            continue

                        # filter request params
                        for f in self.filters:
                            if isinstance(f, str):
                                value = getattr(filters, f)(k, value, r)()
                            elif issubclass(f, BaseFilter):
                                value = f(k, value, r)()

                        if r.callback is not None and isfunction(r.callback):
                            value = r.callback(value)

                        rst[r.key_map or k] = value
                    except ParamsValueError as e:
                        return self._f_resp(e)

                return func(*args, **kwargs)
            return wrapper
        return decorator

    def _f_resp(self, error):
        """ Handler not formatted request error

        :param error: ParamsValueError
        """
        if self.response is not None:
            return self.response()(self.formatter, error)

        if self.content_type == "text/html":
            return HTMLResponse()(self.formatter, error)

        return JSONResponse()(self.formatter, error)
