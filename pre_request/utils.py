# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2020
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-04-27 09:22'


def get_deep_value(key, params, default=None, deep=True):
    """ Extract value from complex structure with deep search

    :param key: special key, use '.' to separate different depth
    :param params: origin data
    :param default: default value if special key is not exists
    :param deep: extract deep value
    """
    if key is None:
        return default

    # extract value from first depth
    if not deep:
        return params.get(key.split(".")[-1], default)

    # invalid input params type
    if not params or not isinstance(params, dict):
        raise ValueError("Can't read deep value from path: '%s'" % key)

    for k in key.split("."):
        params = params.get(k, default)
        if not isinstance(params, dict) and not key.endswith(k):
            raise ValueError("Can't read deep value from path: '%s'" % key)

    return params
