# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2020
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-03-27 14:58'
from pre_request.exception import ParamsValueError
from pre_request.filters.base import BaseFilter


class EqualFilter(BaseFilter):
    """
    判断数值相等过滤器
    """

    eq_code = 478
    neq_code = 479

    def fmt_error_message(self, code):
        """ 格式化错误消息
        """
        if code == 478:
            return f"{self.key} field must be equal to {str(self.rule.eq)}"

        if code == 479:
            return f"{self.key} field cannot be equal to {str(self.rule.neq)}"

        return f"{self.key} field fails the 'EqualFilter' filter check"

    def filter_required(self):
        """ 检查过滤器是否必须执行
        """
        if not self.rule.required and self.value is None:
            return False

        if self.rule.eq is not None:
            return True

        if self.rule.neq is not None:
            return True

        return False

    def __call__(self, *args, **kwargs):
        super().__call__()

        if self.rule.eq is not None and self.value != self.rule.eq:
            raise ParamsValueError(self.eq_code, filter=self)

        if self.rule.neq is not None and self.value == self.rule.neq:
            raise ParamsValueError(self.neq_code, filter=self)

        return self.value
