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
    LocationFilter,
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


simple_filters = [
    EmptyFilter,
    SplitFilter,
    MultiFilter,
    TypeFilter,
    TrimFilter,
    StringFilter,
    RegexpFilter,
    ContentFilter,
    NetworkFilter,
    LocationFilter,
    LengthFilter,
    RangeFilter,
    EqualFilter,
    EnumFilter,
    JsonFilter,
    DefaultFilter,
]


cross_filters = [
    RequiredWithFilter,
    EqualKeyFilter
]
