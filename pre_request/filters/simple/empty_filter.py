# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2019
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-03-17 15:34'
from pre_request.exception import ParamsValueError
from pre_request.filters.base import BaseFilter


class EmptyFilter(BaseFilter):
    """
    判断参数是否为空的过滤器
    """

    def __call__(self, *args, **kwargs):
        super().__call__()

        if self.value is None and self.rule.required:
            raise ParamsValueError(f"{self.key} field cannot be empty")

        return self.value
