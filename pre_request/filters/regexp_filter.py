# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2019
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-03-17 15:38'
import re

from pre_request.exception import ParamsValueError
from pre_request.regexp import Regexp
from .base import BaseFilter


class RegexpFilter(BaseFilter):
    """
    正则表达式过滤器
    """
    error_code = 566

    def __call__(self, *args, **kwargs):
        super(RegexpFilter, self).__call__()

        if self.rule.allow_empty and self.value == self.rule.default:
            return self.value

        # 判断是否需要进行正则匹配
        if self.rule.reg and isinstance(self.rule.reg, str):
            # 判断是否符合正则
            if not Regexp(self.rule.reg, re.IGNORECASE)(self.value):
                raise ParamsValueError(self.error_code, filter=self)
        return self.value
