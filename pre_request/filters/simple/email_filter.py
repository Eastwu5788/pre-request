# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2019
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-03-17 15:46'
from pre_request.exception import ParamsValueError
from pre_request.regexp import EmailRegexp
from pre_request.filters.base import BaseFilter


class EmailFilter(BaseFilter):
    """邮箱过滤器"""
    error_code = 564

    def fmt_error_message(self, _):
        """ 格式化错误信息
        """
        return "%s字段不符合邮件格式!" % self.key

    def filter_required(self):
        """ 验证过滤器是否必须执行
        """
        if not self.rule.required and self.value is None:
            return False

        if not self.rule.email or self.rule.direct_type != str:
            return False

        return True

    def __call__(self, *args, **kwargs):
        super(EmailFilter, self).__call__()

        fmt_value = self.value if isinstance(self.value, list) else [self.value]

        for value in fmt_value:
            if not EmailRegexp()(value):
                raise ParamsValueError(self.error_code, filter=self)

        return self.value
