# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2019
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-03-17 15:44'
from pre_request.exception import ParamsValueError
from .base import BaseFilter


class EnumFilter(BaseFilter):
    """枚举过滤器"""
    error_code = 563

    def __call__(self, *args, **kwargs):
        super(EnumFilter, self).__call__()

        if self.rule.enum and self.value not in self.rule.enum:
            raise ParamsValueError(self.error_code, filter=self)

        return self.value
