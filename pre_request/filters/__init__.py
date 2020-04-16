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
from .equal_filter import EqualFilter
from .mobile_filter import MobileFilter
from .json_filter import JsonFilter
from .default_filter import DefaultFilter
from .content_filter import ContentFilter
from .string_filter import StringFilter
from .file_filter import FileFilter
from .network_filter import NetworkFilter
from .location_filter import LocationFilter

from .equal_key_filter import EqualKeyFilter
from .required_with_filter import RequiredWithFilter

simple_filters = [
    "EmptyFilter",  # 1.判断字段是否为空的过滤器
    "TypeFilter",  # 4.类型转换过滤器
    "TrimFilter",  # 2.去除字符串两侧的空格
    "StringFilter",  # 字符串处理过滤器
    "RegexpFilter",  # 3.正则表达式过滤器
    "ContentFilter",  # 内容检查过滤器
    # "FileFilter",  # 文件路径检查过滤器
    "NetworkFilter",  # 网络检查过滤器
    "LocationFilter",  # 地理位置过滤器
    "LengthFilter",  # 5.字符长度过滤器
    "RangeFilter",  # 6.取值范围过滤器
    "EqualFilter",  # 7.取值相等过滤器
    "EnumFilter",  # 8.枚举过滤器
    "EmailFilter",  # 9.邮箱过滤器
    "MobileFilter",  # 10.手机号过滤器
    "JsonFilter",  # 11.Json解析器
    "DefaultFilter",  # 12.默认值填充
]


complex_filters = [
    "RequiredWithFilter",
    "EqualKeyFilter"
]
