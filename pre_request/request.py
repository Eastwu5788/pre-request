# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2020
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-04-01 09:47'
# sys
import typing as t
from functools import wraps
from inspect import isfunction
from inspect import getfullargspec
# 3p
from flask import (  # pylint: disable=unused-import
    Flask,
    g,
    request,
)
from werkzeug.datastructures import FileStorage
# object
from .exception import ParamsValueError
from .filters import (  # pylint: disable=unused-import
    BaseFilter,
    ContentFilter,
    DefaultFilter,
    EmptyFilter,
    EnumFilter,
    EqualFilter,
    EqualKeyFilter,
    JsonFilter,
    LengthFilter,
    MultiFilter,
    NetworkFilter,
    RangeFilter,
    RegexpFilter,
    RequiredWithFilter,
    SplitFilter,
    StringFilter,
    TypeFilter,
    TrimFilter,
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
from .utils import (
    get_deep_value,
    missing
)
# checking
if t.TYPE_CHECKING:
    from flask import Response  # pylint: disable=unused-import


class PreRequest:
    """ An object to dispatch filters to handler request params
    """

    basic_filters: t.List["BaseFilter"] = [
        EmptyFilter,
        JsonFilter,
        SplitFilter,
        MultiFilter,
        TypeFilter,
    ]

    simple_filters: t.List["BaseFilter"] = [
        TrimFilter,
        StringFilter,
        RegexpFilter,
        ContentFilter,
        NetworkFilter,
        LengthFilter,
        RangeFilter,
        EqualFilter,
        EnumFilter,
        DefaultFilter,
    ]

    cross_filters: t.List["BaseFilter"] = [
        RequiredWithFilter,
        EqualKeyFilter
    ]

    def __init__(
            self,
            app: t.Optional["Flask"] = None,
            fuzzy: bool = False,
            store_key: t.Optional[str] = None,
            content_type: t.Optional[str] = None,
            skip_filter: bool = False
    ):
        """ PreRequest init function

        :param fuzzy: formatter error message with fuzzy style
        :param store_key: which key will store formatter result
        :param content_type: response content type json/html
        :param skip_filter: skip all of the filter check
        """
        self.fuzzy: bool = fuzzy
        self.content_type: str = content_type or "application/json"
        self.store_key: str = store_key or "params"
        self.response: t.Optional[BaseResponse] = None
        self.formatter: t.Optional[t.Callable] = None
        self.skip_filter: bool = skip_filter

        if app is not None:
            self.app: "Flask" = app
            self.init_app(app, None)

    def init_app(self, app: "Flask", config: t.Optional[dict] = None):
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

    def add_response(self, resp: BaseResponse):
        """ Add custom response class

        :param resp: response class which is subclass of BaseResponse
        """
        self.response = resp

    def add_formatter(self, fmt: t.Callable):
        """ Add custom format function for generate response content

        :param fmt: format function
        """
        if fmt and not isfunction(fmt):
            raise TypeError("custom format function must be a type of function")

        if fmt and fmt.__code__.co_argcount < 1:
            raise TypeError("custom format function requires at least 1 arguments")

        self.formatter = fmt

    def add_filter(self, cus_filter: "BaseFilter", index: t.Optional[int] = None):
        """ Add custom filter class to extend pre-request

        :param cus_filter: custom filter class
        :param index: filter position
        """
        if index is not None and not isinstance(index, int):
            raise TypeError("index params must be type of Int")

        if index is not None:
            self.simple_filters.insert(index, cus_filter)
        else:
            self.simple_filters.append(cus_filter)

    def remove_filter(self, cus_filter: t.Optional["BaseFilter"] = None, index: t.Optional[int] = None):
        """ Remove filters from object with index or filter name

        :param cus_filter: user filter name
        :param index: filter index
        """
        if cus_filter:
            self.simple_filters.remove(cus_filter)

        if index is not None and isinstance(index, int) and 0 <= index < len(self.simple_filters):
            self.simple_filters.pop(index)

    @staticmethod
    def _location_params(key, location, default=None, deep=True):
        """ Read params form special location ex: args/forms/header/cookies

        :param key: params key
        :param location: special location
        :param default: default value if special value is not exists
        :param deep: read params with deep search
        """
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

    def _filter_basic_rules(self, k, v, r):
        """ Filter basic rules
        """
        # filter request params
        for f in self.basic_filters:
            obj = f(k, v, r)

            # ignore invalid and not required filter
            if not obj.filter_required():
                continue

            v = obj()

        return v

    def _fmt_params(self, key, rule, default=None):
        """ Query request params from flask request object

        :param key: params key
        """
        df_location = ["values", "args", "form", "json", "headers", "cookies"]

        if len(key.split(".")) > 1 and rule.deep:
            rst = get_deep_value(key, getattr(request, "json"), default, deep=True)
            # load value from depth json struct failed
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
        # load single params
        if not rule.multi:
            return request.files.get(key)

        # load multi files
        params = []
        for f in request.files.getlist(key):
            params.append(f)
        return params

    def _sub_struct_filter(self, k, sub_k, v, r):
        """ Filter sub struct k-v
        """
        sub_v = self._filter_basic_rules(k, v.get(sub_k), r)
        fmt_v = self._handler_simple_filter(k, sub_v, r)
        # The target key needs to be mapped
        return r.key_map if isinstance(r, Rule) and r.key_map else sub_k, fmt_v

    def _handler_sub_struct(self, k, v, r):
        """ Handler filter rules for sub struct

        :param k: params key
        :param v: params value
        :param r: params rule
        """
        # make sure that input value is not empty
        if r.required and not v:
            raise ParamsValueError(message=f"'{k}' field cannot be empty")

        # Invalid struct config
        if not r.multi and not r.json:
            raise TypeError("invalid usage of `struct` params")

        if not v:
            return [] if r.multi else {}

        if isinstance(v, dict):
            fmt_result = {}
            for sub_k, sub_r in r.struct.items():
                fmt_k, fmt_v = self._sub_struct_filter(k + "." + sub_k, sub_k, v, sub_r)
                fmt_result[fmt_k] = fmt_v
            return fmt_result

        # storage sub array
        fmt_result = []
        for idx, sub_v in enumerate(v):
            # make sure that array item must be type of dict
            if not isinstance(sub_v, dict):
                raise ParamsValueError(message="Input " + k + "." + str(idx) + " invalid type")

            # format every k-v with struct
            fmt_item = {}
            fmt_result.append(fmt_item)
            for sub_k, sub_r in r.struct.items():
                fmt_k, fmt_v = self._sub_struct_filter(k + "." + str(idx) + "." + sub_k, sub_k, sub_v, sub_r)
                fmt_item[fmt_k] = fmt_v

        return fmt_result


    def _handler_simple_filter(self, k, v, r):  # noqa
        """ Handler filter rules with simple ways

        :param k: params key
        :param r: params rule
        """
        if isinstance(r, dict):
            fmt_result = {}
            for key, rule in r.items():
                fmt_value = self._handler_simple_filter(k + "." + key, v, rule)
                fmt_result[rule.key_map if isinstance(rule, Rule) and rule.key_map else key] = fmt_value
            return fmt_result

        if not isinstance(r, Rule):
            raise TypeError(f"invalid rule type for key '{k}'")

        if v is None:
            # load file type of params from request
            if r.direct_type == FileStorage:
                v = self._fmt_file_params(k, r)

            # load simple params
            else:
                v = self._fmt_params(k, r, default=missing)

        # Basic filters for every value
        v = v if r.skip or self.skip_filter else self._filter_basic_rules(k, v, r)

        # Filter sub struct
        if r.struct is not None:
            return self._handler_sub_struct(k, v, r)

        if r.skip or self.skip_filter:
            return v

        # filter request params
        for f in self.simple_filters:
            filter_obj = f(k, v, r)

            # ignore invalid and not required filter
            if not filter_obj.filter_required():
                continue

            v = filter_obj()

        if r.callback is not None and isfunction(r.callback):
            v = r.callback(v)

        return v

    def _handler_cross_filter(self, k, r, rst):
        """ Handler complex rule filters

        :param k: params key
        :param r: params rule
        :param rst: handler result
        """
        if isinstance(r, dict):
            for key, value in r.items():
                self._handler_cross_filter(k + "." + key, value, rst)
            return

        if not isinstance(r, Rule):
            raise TypeError(f"invalid rule type for key '{k}'")

        if r.skip or self.skip_filter:
            return

        # simple filter handler
        for f in self.cross_filters:
            filter_obj = f(k, None, r)

            # ignore invalid and not required filter
            if not filter_obj.filter_required():
                continue

            filter_obj(params=rst)

    def parse(
            self,
            rule: t.Optional[t.Dict[str, t.Union["Rule", dict]]] = None,
            **options
    ) -> dict:
        """ Parse input params
        """
        fmt_rst = {}

        # invalid input
        if not rule and not options:
            return fmt_rst

        # query rules with special method
        rules = options.get(request.method) or options.get(request.method.lower())

        # common rule
        if rules is None and rule is not None:
            rules = rule

        # ignore catch with empty rules
        if not rules:
            raise ValueError(f"request method '{request.method}' with invalid filter rule")

        # use simple filter to handler params
        for k, r in rules.items():
            value = self._handler_simple_filter(k, None, r)
            # simple filter handler
            fmt_rst[r.key_map if isinstance(r, Rule) and r.key_map else k] = value

        # use complex filter to handler params
        for k, r in rules.items():
            self._handler_cross_filter(k, r, fmt_rst)

        return fmt_rst

    def catch(
            self,
            rule: t.Optional[t.Dict[str, t.Union["Rule", dict]]] = None,
            **options
    ) -> t.Callable:
        """ Catch request params
        """
        def decorator(func: t.Callable) -> t.Callable:
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

    def fmt_resp(self, error: ParamsValueError) -> "Response":
        """ Handler not formatted request error

        :param error: ParamsValueError
        """
        if self.response is not None:
            return self.response.make_response(error, self.fuzzy, self.formatter)

        if self.content_type == "text/html":
            return HTMLResponse.make_response(error, self.fuzzy, self.formatter)

        return JSONResponse.make_response(error, self.fuzzy, self.formatter)
