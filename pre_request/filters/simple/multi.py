# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2020
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-05-12 09:56'
from pre_request.filters.base import BaseFilter
from pre_request.utils import missing
from pre_request.exception import ParamsValueError


class MultiFilter(BaseFilter):
    """ 处理多值的过滤器
    """

    def __call__(self, *args, **kwargs):
        super().__call__()

        if self.rule.multi and not isinstance(self.value, list):
            # empty input, and required is false
            if self.value is missing or self.value is None:
                return []

            raise ParamsValueError(f"'{self.key}' must by type of array")

        return self.value
