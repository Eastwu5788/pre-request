# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2020
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-03-27 14:58'
from pre_request.exception import ParamsValueError
from pre_request.filters.base import BaseFilter
from pre_request.utils import missing


class EqualFilter(BaseFilter):
    """
    判断数值相等过滤器
    """

    def filter_required(self):
        """ 检查过滤器是否必须执行
        """
        if not self.rule.required and (self.value is missing and self.value is None):
            return False

        if self.rule.eq is not None:
            return True

        if self.rule.neq is not None:
            return True

        return False

    def __call__(self, *args, **kwargs):
        super().__call__()

        if self.rule.eq is not None and self.value != self.rule.eq:
            raise ParamsValueError(f"'{self.key}' should be equal to '{self.rule.eq}'")

        if self.rule.neq is not None and self.value == self.rule.neq:
            raise ParamsValueError(f"'{self.key}' should be equal to '{self.rule.neq}'")

        return self.value
