# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2019
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-03-17 15:44'
from pre_request.exception import ParamsValueError
from pre_request.filters.base import BaseFilter


class EnumFilter(BaseFilter):
    """枚举过滤器"""
    error_code = 563

    def fmt_error_message(self, _):
        """ 格式化错误消息
        """
        return "%s字段的取值只能是以下几种%s!" % (self.key, str(self.rule.enum))

    def filter_required(self):
        """ 检查过滤器是否必须执行
        """
        if not self.rule.required and self.value is None:
            return False

        if self.rule.enum and not isinstance(self.value, (list, dict)):
            return True

        return False

    def __call__(self, *args, **kwargs):
        super(EnumFilter, self).__call__()

        if self.value not in self.rule.enum:
            raise ParamsValueError(self.error_code, filter=self)

        return self.value
