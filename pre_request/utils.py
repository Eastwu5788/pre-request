# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2020
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-04-27 09:22'


def get_deep_value(key, params, default=None, deep=True):
    """ 获取多层嵌套的参数值

    :param key: 多层次的key
    :param params: 读取的数据源
    :param default: 默认值
    :param deep: 是否进行深度递归查询
    """
    if key is None:
        return default

    # 不进行深度递归查询，直接返回最后一层结果
    if not deep:
        return params.get(key.split(".")[-1], default)

    # 无效的入参
    if not params or not isinstance(params, dict):
        raise ValueError("Can't read deep value from path: '%s'" % key)

    for k in key.split("."):
        params = params.get(k, default)
        if not isinstance(params, dict) and not key.endswith(k):
            raise ValueError("Can't read deep value from path: '%s'" % key)

    return params
