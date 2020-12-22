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
# 3p
from flask import g
from werkzeug.datastructures import FileStorage
# object
from .exception import ParamsValueError
from .filters.base import BaseFilter
from .filters import (
    complex_filters,
    simple_filters,
)
from .macro import (
    K_CONTENT_TYPE,
    K_FUZZY,
    K_SKIP_FILTER,
    K_STORE_KEY
)
from .response import (
    BaseResponse,
    HTMLResponse,
    JSONResponse,
)
from .rules import Rule
from .utils import get_deep_value
from . import filters


class PreRequest:
    """ An object to dispatch filters to handler request params
    """

    def __init__(self, app=None, fuzzy=False, store_key=None, content_type=None, skip_filter=False):
        """ PreRequest init function

        :param fuzzy: formatter error message with fuzzy style
        :param store_key: which key will store formatter result
        :param content_type: response content type json/html
        :param skip_filter: skip all of the filter check
        """
        self.filters = simple_filters
        self.complex_filters = complex_filters
        self.fuzzy = fuzzy
        self.content_type = content_type or "application/json"
        self.store_key = store_key or "params"
        self.response = None
        self.formatter = None
        self.skip_filter = skip_filter

        if app is not None:
            self.app = app
            self.init_app(app, None)

    def init_app(self, app, config=None):
        """ Flask extension initialize

        :param app: flask application
        :param config: flask config
        """
        if not (config is None or isinstance(config, dict)):
            raise TypeError("'config' params must be type of dict or None")

        # update config from different origin
        basic_config = app.config.copy()
        if config:
            basic_config.update(config)
        config = basic_config

        self.fuzzy = config.get(K_FUZZY, False)
        self.content_type = config.get(K_CONTENT_TYPE, "application/json")
        self.store_key = config.get(K_STORE_KEY, "params")
        self.skip_filter = config.get(K_SKIP_FILTER, False)

        self.app = app
        app.extensions["pre_request"] = self

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
        """ Remove filters from object with index or filter name

        :param cus_filter: user filter name
        :param index: filter index
        """
        if cus_filter and (isinstance(cus_filter, str) or issubclass(cus_filter, BaseFilter)):
            self.filters.remove(cus_filter)

        if index is not None and isinstance(index, int) and 0 <= index < len(self.filters):
            self.filters.pop(index)

    @staticmethod
    def _location_params(key, location, default=None, deep=True):
        """ Read params form special location ex: args/forms/header/cookies

        :param key: params key
        :param location: special location
        :param default: default value if special value is not exists
        :param deep: read params with deep search
        """
        from flask import request  # pylint: disable=import-outside-toplevel

        location = location.lower()

        if location in ["args", "values", "form", "headers", "cookies"]:
            # query deep value with special key like `userInfo.userId`
            if len(key.split(".")) > 1 and deep:
                return getattr(request, location).get(key, default)
            # load simple params
            return get_deep_value(key, getattr(request, location), default, deep=False)

        if location == "json":
            json_value = getattr(request, location)
            if isinstance(json_value, dict):
                # query deep value with special key like `userInfo.userId`
                if len(key.split(".")) > 1 and deep:
                    return json_value.get(key, default)
                # query simple value from json
                return get_deep_value(key, json_value, default, deep=deep)

        return default

    def _fmt_params(self, key, rule, default=None):
        """ Query request params from flask request object

        :param key: params key
        """
        df_location = ["values", "args", "form", "json", "headers", "cookies"]
        from flask import request  # pylint: disable=import-outside-toplevel

        if len(key.split(".")) > 1 and rule.deep:
            rst = get_deep_value(key, getattr(request, "json"), default, deep=True)
            # load value from depth json structure failed
            if rst != default:
                return rst

        rule.location = rule.location or df_location

        # query object from special location
        for location in rule.location:
            rst = self._location_params(key, location, default, rule.deep)
            # can't read params from this location
            if rst != default:
                return rst

        return default

    @staticmethod
    def _fmt_file_params(key, rule):
        """ Query file params from request.files

        :param key: params key
        :param rule: params rule
        """
        from flask import request  # pylint: disable=import-outside-toplevel

        # load single params
        if not rule.multi:
            return request.files.get(key)

        # load multi files
        fmt_params = list()
        for f in request.files.getlist(key):
            fmt_params.append(f)
        return fmt_params

    def _handler_simple_filter(self, k, v, r):  # noqa
        """ Handler filter rules with simple ways

        :param k: params key
        :param r: params rule
        """
        if isinstance(r, dict):
            fmt_result = dict()
            for key, rule in r.items():
                fmt_value = self._handler_simple_filter(k + "." + key, v, rule)
                fmt_result[rule.key_map if isinstance(rule, Rule) and rule.key_map else key] = fmt_value

            return fmt_result

        if not isinstance(r, Rule):
            raise TypeError("invalid rule type for key '%s'" % k)

        if v is None:
            # load file type of params from request
            if r.direct_type == FileStorage:
                v = self._fmt_file_params(k, r)

            # load simple params
            else:
                v = self._fmt_params(k, r)

        if r.structure is not None:
            # make sure that input value is not empty
            if r.required and not v:
                raise ParamsValueError(560, message="%s field cannot be empty" % k)

            if not r.multi:
                raise TypeError("invalid usage of `structure` params")

            # structure params must be type of list
            if not isinstance(v, list):
                raise ParamsValueError(601, message="Input " + k + " invalid type")

            if not v:
                return list()

            # storage sub array
            fmt_result = list()
            for idx, sub_v in enumerate(v):
                # make sure that array item must be type of dict
                if not isinstance(sub_v, dict):
                    raise ParamsValueError(600, message="Input " + k + "." + str(idx) + " invalid type")

                # format every k-v with structure
                fmt_item = dict()
                fmt_result.append(fmt_item)
                for sub_k, sub_r in r.structure.items():
                    new_k = k + "." + str(idx) + "." + sub_k
                    v = self._handler_simple_filter(new_k, sub_v.get(sub_k), sub_r)
                    fmt_item[sub_r.key_map if isinstance(sub_r, Rule) and sub_r.key_map else sub_k] = v

            return fmt_result

        if r.skip or self.skip_filter:
            return v

        # filter request params
        for f in self.filters:
            filter_obj = None
            # system filter object
            if isinstance(f, str):
                filter_obj = getattr(filters, f)(k, v, r)

            # custom filter object
            elif issubclass(f, BaseFilter):
                filter_obj = f(k, v, r)

            # ignore invalid and not required filter
            if not filter_obj or not filter_obj.filter_required():
                continue

            v = filter_obj()

        if r.callback is not None and isfunction(r.callback):
            v = r.callback(v)

        return v

    def _handler_complex_filter(self, k, r, rst):
        """ Handler complex rule filters

        :param k: params key
        :param r: params rule
        :param rst: handler result
        :param rules: request rules
        """
        if isinstance(r, dict):
            for key, value in r.items():
                self._handler_complex_filter(k + "." + key, value, rst)
            return

        if not isinstance(r, Rule):
            raise TypeError("invalid rule type for key '%s'" % k)

        if r.skip or self.skip_filter:
            return

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

            filter_obj(params=rst)

    def parse(self, rule=None, **options):
        """ Parse input params
        """
        fmt_rst = dict()

        # invalid input
        if not rule and not options:
            return fmt_rst

        # query rules with special method
        from flask import request  # pylint: disable=import-outside-toplevel
        rules = options.get(request.method) or options.get(request.method.lower())

        # common rule
        if rules is None and rule is not None:
            rules = rule

        # ignore catch with empty rules
        if not rules:
            raise ValueError("request method '%s' with invalid filter rule" % request.method)

        # use simple filter to handler params
        for k, r in rules.items():
            value = self._handler_simple_filter(k, None, r)
            # simple filter handler
            fmt_rst[r.key_map if isinstance(r, Rule) and r.key_map else k] = value

        # use complex filter to handler params
        for k, r in rules.items():
            self._handler_complex_filter(k, r, fmt_rst)

        return fmt_rst

    def catch(self, rule=None, **options):
        """ Catch request params
        """
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                # ignore with empty rule
                if not rule and not options:
                    return func(*args, **kwargs)

                # parse input params
                try:
                    fmt_rst = self.parse(rule, **options)
                except ParamsValueError as e:
                    return self.fmt_resp(e)

                # assignment params to func args
                setattr(g, self.store_key, fmt_rst)
                if self.store_key in getfullargspec(func).args:
                    kwargs[self.store_key] = fmt_rst

                return func(*args, **kwargs)
            return wrapper
        return decorator

    def fmt_resp(self, error):
        """ Handler not formatted request error

        :param error: ParamsValueError
        """
        if self.response is not None:
            return self.response()(self.fuzzy, self.formatter, error)

        if self.content_type == "text/html":
            return HTMLResponse()(self.fuzzy, self.formatter, error)

        return JSONResponse()(self.fuzzy, self.formatter, error)
