# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2019
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-03-17 15:36'
from .base import BaseFilter


class TrimFilter(BaseFilter):
    """ 去除字符串前后空格的过滤器
    """

    def filter_required(self):
        """ 检查过滤器是否必须执行
        """
        if not self.rule.required and self.value is None:
            return False

        if self.rule.trim and isinstance(self.value, str):
            return True

        return False

    def __call__(self, *args, **kwargs):
        super(TrimFilter, self).__call__()
        return self.value.strip()
