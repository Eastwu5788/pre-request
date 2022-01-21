# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2020
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-04-10 16:41'
from pre_request.exception import ParamsValueError
from pre_request.filters.base import BaseFilter
from pre_request.utils import missing


class ContentFilter(BaseFilter):
    """ 字符串内容检查过滤器
    """

    def filter_required(self):
        """ 验证过滤器是否必须执行
        """
        if not self.rule.required and (self.value is missing or self.value is None):
            return False

        if not isinstance(self.value, str):
            return False

        if self.rule.contains or self.rule.contains_any:
            return True

        if self.rule.startswith or self.rule.endswith:
            return True

        if self.rule.excludes:
            return True

        return False

    def __call__(self, *args, **kwargs):
        super().__call__()

        if self.rule.startswith and not self.value.startswith(self.rule.startswith):
            raise ParamsValueError(f"'{self.key}' should start with '{self.rule.startswith}'")

        if self.rule.endswith and not self.value.endswith(self.rule.endswith):
            raise ParamsValueError(f"'{self.key}' should end with '{self.rule.startswith}'")

        for contain in self.rule.contains:
            if contain not in self.value:
                raise ParamsValueError(f"'{self.key}' need required content")

        for contain in self.rule.excludes:
            if contain in self.value:
                raise ParamsValueError(f"'{self.key}' contain prohibited content")

        for contain in self.rule.contains_any:
            if contain in self.value:
                return self.value

        if self.rule.contains_any:
            raise ParamsValueError(f"'{self.key}' should contain special content")

        return self.value
