# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2019
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-03-17 15:46'
from pre_request.exception import ParamsValueError
from pre_request.regexp import EmailRegexp
from .base import BaseFilter


class EmailFilter(BaseFilter):
    """邮箱过滤器"""
    error_code = 564

    def __call__(self, *args, **kwargs):
        super(EmailFilter, self).__call__()

        if self.rule.email:
            if not EmailRegexp()(self.value):
                raise ParamsValueError(self.error_code, filter=self)

        return self.value
