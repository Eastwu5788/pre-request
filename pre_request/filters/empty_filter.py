# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2019
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-03-17 15:34'
from pre_request.exception import ParamsValueError
from .base import BaseFilter


class EmptyFilter(BaseFilter):
    """
    判断参数是否为空的过滤器
    """
    error_code = 560

    def __call__(self, *args, **kwargs):
        super(EmptyFilter, self).__call__()

        # 参数输入值为空
        # BUG: 只有用户不输入的情况下才为None，判断为空应该是当前这种情况
        # 如果是 not self.value 则包括了多种false情况
        if self.value is None:
            if self.rule.allow_empty:
                self.value = self.rule.default
            else:
                raise ParamsValueError(self.error_code, filter=self)
        return self.value
