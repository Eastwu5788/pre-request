# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2019
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-03-17 15:37'
from pre_request.exception import ParamsValueError
from pre_request.filters.base import BaseFilter


class LengthFilter(BaseFilter):
    """
    判断字符串长度的过滤器
    """

    length_code_gt = 474
    length_code_gte = 475
    length_code_lt = 476
    length_code_lte = 477
    illegal_code = 480

    def fmt_error_message(self, code):
        """ 格式化错误消息
        """
        if code == 474:
            return f"{self.key} field content length must be greater than {str(self.rule.gt)}"

        if code == 475:
            return f"{self.key} field content length must be greater than or equal to {str(self.rule.gte)}"

        if code == 476:
            return f"{self.key} field content length must be less than {str(self.rule.lt)}"

        if code == 477:
            return f"{self.key} field content length must be less than or equal to {str(self.rule.lte)}"

        return f"{self.key} field fails the 'LengthFilter' filter check"

    def filter_required(self):
        """ 检查过滤器是否必须执行
        """
        if not self.rule.required and self.value is None:
            return False

        if self.rule.direct_type not in [str, list]:
            return False

        if self.rule.gt is not None:
            return True

        if self.rule.gte is not None:
            return True

        if self.rule.lt is not None:
            return True

        if self.rule.lte is not None:
            return True

        return False

    def __call__(self, *args, **kwargs):
        super().__call__()

        fmt_value = self.value if isinstance(self.value, list) else [self.value]

        for value in fmt_value:
            # 大于
            if self.rule.gt is not None and not len(value) > self.rule.gt:
                raise ParamsValueError(self.length_code_gt, filter=self)

            # 大于等于
            if self.rule.gte is not None and not len(value) >= self.rule.gte:
                raise ParamsValueError(self.length_code_gte, filter=self)

            # 小于
            if self.rule.lt is not None and not len(value) < self.rule.lt:
                raise ParamsValueError(self.length_code_lt, filter=self)

            # 小于等于
            if self.rule.lte is not None and not len(value) <= self.rule.lte:
                raise ParamsValueError(self.length_code_lte, filter=self)

        return self.value
