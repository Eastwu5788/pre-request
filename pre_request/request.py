# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2020
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-04-01 09:47'
# sys
from functools import wraps
from inspect import isfunction
from inspect import getfullargspec

# object
from .exception import ParamsValueError
from .filters.base import BaseFilter
from .filters import simple_filters, complex_filters
from .response import JSONResponse, HTMLResponse, BaseResponse
from .rules import Rule
from . import filters


class PreRequest:
    """ An object to dispatch filters to handler request params
    """

    def __init__(self, content_type=None):
        self.filters = simple_filters
        self.complex_filters = complex_filters
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
    def _location_params(key, location, default=None):
        """ 读取指定位置的参数

        :param key: 数据的key
        :param location: 读取数据的位置
        :param default: 未读取到时的默认值
        """
        from flask import request  # pylint: disable=import-outside-toplevel

        location = location.lower()

        if location in ["args", "values", "form", "headers", "cookies"]:
            return getattr(request, location).get(key, default)

        if location == "json":
            json_value = getattr(request, location)
            if isinstance(json_value, dict):
                return json_value.get(key, default)

        return default

    def _fmt_params(self, key, rule, default=None):
        """ Query request params from flask request object

        :param key: params key
        """
        # query params from special location
        if rule.location is not None:
            for location in rule.location:
                rst = self._location_params(key, location, default)
                if rst != default:
                    return rst
            return default

        # query params from simple method
        from flask import request  # pylint: disable=import-outside-toplevel
        value = request.values.get(key, default)
        if value is not None:
            return value

        # query params from json request
        json_value = getattr(request, "json")
        if json_value and isinstance(json_value, dict):
            return json_value.get(key, default)

        return default

    def _handler_simple_filter(self, rules, rst):
        """ 处理普通过滤器

        :param rules: 参数规则
        :param rst: 格式化后的结果值
        """
        for k, r in rules.items():
            # invalid rule
            if not isinstance(r, Rule):
                raise TypeError("invalid rule type for key '%s'" % k)

            value = self._fmt_params(k, r)

            # skip filter
            if r.skip:
                rst[r.key_map or k] = value
                continue

            try:
                # filter request params
                for f in self.filters:
                    filter_obj = None
                    # system filter object
                    if isinstance(f, str):
                        filter_obj = getattr(filters, f)(k, value, r)

                    # custom filter object
                    elif issubclass(f, BaseFilter):
                        filter_obj = f(k, value, r)

                    # ignore invalid and not required filter
                    if not filter_obj or not filter_obj.filter_required():
                        continue

                    value = filter_obj()

                if r.callback is not None and isfunction(r.callback):
                    value = r.callback(value)

                # simple filter handler
                rst[r.key_map or k] = value
            except ParamsValueError as e:
                return self._f_resp(e)

        return None

    def _handler_complex_filter(self, rules, params):
        """ 处理复合过滤器

        :param rules: 参数规则
        :param params: 所有合规参数
        """
        for k, r in rules.items():
            # skip filter
            if r.skip:
                continue

            try:
                # simple filter handler
                for f in self.complex_filters:
                    filter_obj = None
                    # system filter object
                    if isinstance(f, str):
                        filter_obj = getattr(filters, f)(k, None, r)

                    # custom filter object
                    elif issubclass(f, BaseFilter):
                        filter_obj = f(k, None, r)

                    # ignore invalid and not required filter
                    if not filter_obj or not filter_obj.filter_required():
                        continue

                    filter_obj(params=params)
            except ParamsValueError as e:
                return self._f_resp(e)

        return None

    def catch(self, rule=None, **options):
        """ Catch request params
        """
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                from flask import g, request  # pylint: disable=import-outside-toplevel

                g.params = rst = dict()

                # ignore with empty rule
                if not rule and not options:
                    return func(*args, **kwargs)

                # query rules with special method
                rules = options.get(request.method) or options.get(request.method.lower())

                # common rule
                if rules is None and rule is not None:
                    rules = rule

                # ignore catch with empty rules
                if not rules:
                    raise ValueError("request method '%s' with invalid filter rule" % request.method)

                # use simple filter to handler params
                resp = self._handler_simple_filter(rules, rst)
                if resp is not None:
                    return resp

                # use complex filter to handler params
                resp = self._handler_complex_filter(rules, rst)
                if resp is not None:
                    return resp

                # assignment params to func args
                if "params" in getfullargspec(func).args:
                    kwargs["params"] = rst

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
