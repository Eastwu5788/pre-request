# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2019
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-03-17 15:34'
from pre_request.exception import ParamsValueError
from pre_request.filters.base import BaseFilter
from pre_request.utils import missing


class EmptyFilter(BaseFilter):
    """
    判断参数是否为空的过滤器
    """

    def __call__(self, *args, **kwargs):
        super().__call__()

        if self.rule.required and (self.value is missing or self.value is None):
            raise ParamsValueError(f"'{self.key}' can't be empty")

        return self.value
