# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2019
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-03-17 15:45'
from pre_request.exception import ParamsValueError
from .base import BaseFilter


class RangeFilter(BaseFilter):
    """取值范围过滤器"""

    range_code_gt = 568
    range_code_gte = 571
    range_code_lt = 572
    range_code_lte = 573

    def __call__(self, *args, **kwargs):
        super(RangeFilter, self).__call__()

        # 默认值过滤
        if self.rule.allow_empty and self.value == self.rule.default:
            return self.value

        # 允许为空值时的过滤
        if self.rule.allow_empty and self.value is None:
            return self.value

        # Range 范围判断仅针对`int`, `float` 类型有效
        if self.rule.direct_type not in [int, float]:
            return self.value

        # 大于
        if self.rule.gt is not None and not self.value > self.rule.gt:
            raise ParamsValueError(self.range_code_gt, filter=self)

        # 大于等于
        if self.rule.gte is not None and not self.value >= self.rule.gte:
            raise ParamsValueError(self.range_code_gte, filter=self)

        # 小于
        if self.rule.lt is not None and not self.value < self.rule.lt:
            raise ParamsValueError(self.range_code_lt, filter=self)

        # 小于等于
        if self.rule.lte is not None and not self.value <= self.rule.lte:
            raise ParamsValueError(self.range_code_lte, filter=self)

        return self.value
