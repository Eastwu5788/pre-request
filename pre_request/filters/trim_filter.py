# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2019
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-03-17 15:36'
from .base import BaseFilter


class TrimFilter(BaseFilter):
    """
    去除字符串前后空格的过滤器
    """
    error_code = 569

    def __call__(self, *args, **kwargs):
        super(TrimFilter, self).__call__()

        if self.rule.trim and isinstance(self.value, str):
            return self.value.strip()
        return self.value
