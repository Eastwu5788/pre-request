# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2020
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-04-10 16:59'
from .base import BaseFilter


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

        if self.rule.lower:
            self.value = self.value.lower()

        if self.rule.upper:
            self.value = self.value.upper()

        return self.value
