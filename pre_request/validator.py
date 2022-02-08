# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2021
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2022/2/8 10:21 上午'
# sys
import typing as t
from functools import wraps
from inspect import getfullargspec
# project
from .core import Core
from .rules import Rule


class Validator(Core):

    def __init__(self, params: t.Optional[t.Dict] = None, **kwargs):
        super().__init__(**kwargs)
        self.params = params

    def get_value(self, k, r, default=None):
        """ Get value from params
        """
        if len(k.split(".")) > 1 and r.deep:
            rst = self.extract_value(self.params, k, default, deep=True)
            # load value from depth json struct failed
            if rst != default:
                return rst

        return self.params.get(k, default)

    def validate(self):
        fmt_rst = {}
        # use simple filter to handler params
        for k, r in self.rule.items():
            value = self.handler_simple_filters(k, None, r)
            # simple filter handler
            fmt_rst[r.key_map if isinstance(r, Rule) and r.key_map else k] = value

        # use complex filter to handler params
        for k, r in self.rule.items():
            self.handler_cross_filter(k, r, fmt_rst)

        return fmt_rst


def validator(
        rule: t.Optional[t.Dict[str, t.Union["Rule", dict]]] = None
) -> t.Callable:
    """ Validate function params
    """
    def decorator(func: t.Callable) -> t.Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not rule:
                return func(*args, **kwargs)

            # get all args from function
            args_key = getfullargspec(func).args

            # get all default value
            dft_args = func.__defaults__
            kw = {} if not dft_args else dict(zip(args_key[len(args_key) - len(dft_args):], dft_args))

            args_val = args
            if "cls" in args_key or "self" in args_key:
                args_val = args[1:]
                args_key = args_key[1: len(args_val) + 1]
            kw = dict(kw, **dict(zip(args_key, args_val)), **kwargs)

            # Validate function params
            fmt_rst = Validator(rule=rule, params=kw).validate()

            fmt_args = [fmt_rst.pop(args_key[idx]) for idx, _ in enumerate(args)]
            return func(*fmt_args, **dict(kwargs, **fmt_rst))
        return wrapper
    return decorator
