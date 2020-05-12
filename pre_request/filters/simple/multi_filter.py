# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2020
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-05-12 09:56'
from pre_request.filters.base import BaseFilter


class MultiFilter(BaseFilter):
    """ 处理多值的过滤器
    """

    def __call__(self, *args, **kwargs):
        super(MultiFilter, self).__call__()

        if self.rule.multi and not isinstance(self.value, list):
            return [self.value]

        if not self.rule.multi and isinstance(self.value, list):
            return self.value[-1] if self.value else None

        return self.value
