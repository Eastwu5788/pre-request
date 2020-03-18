# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2019
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-03-17 15:37'
from pre_request.exception import ParamsValueError
from .base import BaseFilter


class LengthFilter(BaseFilter):
    """
    判断字符串长度的过滤器
    """
    error_code = 561

    def __call__(self, *args, **kwargs):
        super(LengthFilter, self).__call__()

        if self.rule.len and self.rule.len.need_check():
            if self.rule.allow_empty and not self.value:
                return self.value

            # 长度检查过滤器仅对字符串有效
            if not isinstance(self.value, str):
                raise ParamsValueError(self.error_code, filter=self)

            # 检查结果
            if not self.rule.len.check_length(self.value):
                raise ParamsValueError(self.error_code, filter=self)

        return self.value
