# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2019
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-03-17 15:34'
from pre_request.exception import ParamsValueError
from pre_request.filters.base import BaseFilter


class EmptyFilter(BaseFilter):
    """
    判断参数是否为空的过滤器
    """
    error_code = 560

    def fmt_error_message(self, _):
        """ 格式化错误消息
        """
        return "%s字段不能为空!" % self.key

    def __call__(self, *args, **kwargs):
        super(EmptyFilter, self).__call__()

        if self.value is None and self.rule.required:
            raise ParamsValueError(self.error_code, filter=self)

        return self.value
