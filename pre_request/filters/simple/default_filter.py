# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2020
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-04-10 13:44'
from pre_request.filters.base import BaseFilter


class DefaultFilter(BaseFilter):
    """ 填充默认值的过滤器
    """

    def __call__(self, *args, **kwargs):
        super(DefaultFilter, self).__call__()

        if not self.rule.required and self.value is None:
            self.value = self.rule.default

        return self.value
