# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2019
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-03-17 15:34'

from .empty_filter import EmptyFilter
from .trim_filter import TrimFilter
from .length_filter import LengthFilter
from .regexp_filter import RegexpFilter
from .type_filter import TypeFilter
from .range_filter import RangeFilter
from .enum_filter import EnumFilter
from .email_filter import EmailFilter
from .mobile_filter import MobileFilter
from .json_filter import JsonFilter


__all__ = [
    "EmptyFilter",  # 1.判断字段是否为空的过滤器
    "TrimFilter",  # 2.去除字符串两侧的空格
    "LengthFilter",  # 3.字符长度过滤器
    "RegexpFilter",  # 4.正则表达式过滤器
    "TypeFilter",  # 5.类型转换过滤器
    "RangeFilter",  # 6.取值范围过滤器
    "EnumFilter",  # 7.枚举过滤器
    "EmailFilter",  # 8.邮箱过滤器
    "MobileFilter",  # 9.手机号过滤器
    "JsonFilter",  # 10.Json解析器
]
