# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2021
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2022/2/8 8:36 上午'
# sys
import typing as t
from inspect import isfunction
# project
from .exception import ParamsValueError
from .rules import Rule
from .utils import (
    missing
)
from .filters import (
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


class Core:

    basic_filters: t.List[t.Any] = [
        EmptyFilter,
        JsonFilter,
        SplitFilter,
        MultiFilter,
        TypeFilter,
    ]

    simple_filters: t.List[t.Any] = [
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

    cross_filters: t.List[t.Any] = [
        RequiredWithFilter,
        EqualKeyFilter
    ]

    def __init__(
            self,
            rule: t.Optional[t.Dict[str, t.Union["Rule", dict]]] = None,
            skip_filter: bool = False
    ) -> None:
        self.rule: t.Optional[t.Dict[str, t.Union["Rule", dict]]] = rule
        self.skip_filter: bool = skip_filter

    def get_value(self, k, r, default=None):
        """ Get value from request params
        """
        raise NotImplementedError()

    def handler_sub_struct_filters(self, k, sub_k, v, r):
        """ Filter sub struct k-v
        """
        sub_v = self.handler_basic_filters(k, v.get(sub_k), r)
        fmt_v = self.handler_simple_filters(k, sub_v, r)
        # The target key needs to be mapped
        return r.key_map if isinstance(r, Rule) and r.key_map else sub_k, fmt_v

    def handler_sub_struct(self, k, v, r):
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
                fmt_k, fmt_v = self.handler_sub_struct_filters(k + "." + sub_k, sub_k, v, sub_r)
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
                fmt_k, fmt_v = self.handler_sub_struct_filters(k + "." + str(idx) + "." + sub_k, sub_k, sub_v, sub_r)
                fmt_item[fmt_k] = fmt_v

        return fmt_result

    def handler_simple_filters(self, k, v, r):  # noqa
        """ Handler simple filters
        """
        if isinstance(r, dict):
            fmt_result = {}
            for key, rule in r.items():
                fmt_value = self.handler_simple_filters(k + "." + key, v, rule)
                fmt_result[rule.key_map if isinstance(rule, Rule) and rule.key_map else key] = fmt_value
            return fmt_result

        if not isinstance(r, Rule):
            raise TypeError(f"invalid rule type for key '{k}'")

        if v is None:
            v = self.get_value(k, r, default=missing)

            # Basic filters for every value
        v = v if r.skip or self.skip_filter else self.handler_basic_filters(k, v, r)

        # Filter sub struct
        if r.struct is not None:
            return self.handler_sub_struct(k, v, r)

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

    def handler_basic_filters(self, k, v, r):
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

    def handler_cross_filter(self, k, r, rst):
        """ Handler complex rule filter
        """
        if isinstance(r, dict):
            for key, value in r.items():
                self.handler_cross_filter(k + "." + key, value, rst)
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

    @staticmethod
    def extract_value(
            kw: dict,
            k: str,
            default: t.Optional[t.Any] = None,
            deep: bool = True
    ) -> t.Any:
        """ Extract value from complex structure with deep search

        :param kw: origin data
        :param k: special key, use '.' to separate different depth
        :param default: default value if special key is not exists
        :param deep: extract deep value
        """
        if k is None:
            return default

        # extract value from first depth
        if not deep:
            return kw.get(k.split(".")[-1], default)

        # invalid input params type
        if not isinstance(kw, dict):
            raise ValueError(f"Can't read deep value from path: '{k}'")

        if not kw:
            return default

        for sub_k in k.split("."):
            kw = kw.get(sub_k, default)
            # return dict in deep query
            if not k.endswith(sub_k) and not isinstance(kw, dict):
                kw = {}

        return kw
