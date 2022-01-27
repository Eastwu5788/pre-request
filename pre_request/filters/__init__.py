# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2019
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-03-17 15:34'
# flake8: noqa
from .simple import (
    ContentFilter,
    DefaultFilter,
    EmptyFilter,
    EnumFilter,
    EqualFilter,
    JsonFilter,
    LengthFilter,
    MultiFilter,
    NetworkFilter,
    RangeFilter,
    RegexpFilter,
    SplitFilter,
    StringFilter,
    TrimFilter,
    TypeFilter
)
from .cross import (
    EqualKeyFilter,
    RequiredWithFilter,
)


basic_filters = [
    EmptyFilter,
    SplitFilter,
    MultiFilter,
    TypeFilter,
    JsonFilter,
]


simple_filters = [
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


cross_filters = [
    RequiredWithFilter,
    EqualKeyFilter
]
