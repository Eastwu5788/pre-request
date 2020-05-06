# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2020
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-04-10 16:59'
from pre_request.filters.base import BaseFilter


class StringFilter(BaseFilter):
    """ 字符串处理过滤器
    """

    def filter_required(self):
        """ 验证过滤器是否必须执行
        """
        if not self.rule.required and self.value is None:
            return False

        if self.rule.direct_type != str:
            return False

        if self.rule.lower or self.rule.upper:
            return True

        return False

    def __call__(self, *args, **kwargs):
        super(StringFilter, self).__call__()

        if isinstance(self.value, str):
            return self.value.lower() if self.rule.lower else self.value.upper()

        if isinstance(self.value, list):
            return [value.lower() if self.rule.lower else value.upper() for value in self.value]

        return self.value
