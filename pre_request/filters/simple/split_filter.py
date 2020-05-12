# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2020
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-04-26 10:50'
from pre_request.filters.base import BaseFilter


class SplitFilter(BaseFilter):
    """参数分割过滤器"""

    def filter_required(self):
        """ 检查过滤器是否必须执行
        """
        if not self.rule.required and self.value is None:
            return False

        if self.rule.split is not None and isinstance(self.value, str):
            return True

        return False

    def __call__(self, *args, **kwargs):
        super(SplitFilter, self).__call__()
        return self.value.split(self.rule.split)
