# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2019
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-03-17 15:44'
from pre_request.exception import ParamsValueError
from pre_request.filters.base import BaseFilter
from pre_request.utils import missing


class EnumFilter(BaseFilter):
    """枚举过滤器"""

    def filter_required(self):
        """ 检查过滤器是否必须执行
        """
        if not self.rule.required and self.value is missing:
            return False

        if isinstance(self.value, list) and not self.rule.multi:
            return False

        if self.rule.enum:
            return True

        return False

    def __call__(self, *args, **kwargs):
        super().__call__()

        for v in self.value if isinstance(self.value, list) else [self.value]:
            if v not in self.rule.enum:
                raise ParamsValueError(f"'{self.key}' must be one of the following '{self.rule.enum}'")

        return self.value
