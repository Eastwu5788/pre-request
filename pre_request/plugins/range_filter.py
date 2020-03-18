# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2019
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-03-17 15:45'
from pre_request.exception import ParamsValueError
from .base import BaseFilter


class RangeFilter(BaseFilter):
    """取值范围过滤器"""
    error_code = 567
    range_code = 568

    def __call__(self, *args, **kwargs):
        super(RangeFilter, self).__call__()

        if self.rule.range.need_check():
            try:
                if not self.rule.range.check_range(self.value):
                    raise ParamsValueError(self.error_code, filter=self)
            except TypeError:
                raise ParamsValueError(self.range_code, filter=self)

        return self.value
