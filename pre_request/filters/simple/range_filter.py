# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2019
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-03-17 15:45'
# sys
import datetime
from decimal import Decimal
# project
from pre_request.exception import ParamsValueError
from pre_request.filters.base import BaseFilter


class RangeFilter(BaseFilter):
    """取值范围过滤器"""

    range_code_gt = 568
    range_code_gte = 571
    range_code_lt = 572
    range_code_lte = 573

    def fmt_error_message(self, code):
        """ 格式化错误消息
        """
        if code == 568:
            return "%s field value must be greater than %s" % (self.key, str(self.rule.gt))

        if code == 571:
            return "%s field value must be greater than or equal to %s" % (self.key, str(self.rule.gte))

        if code == 572:
            return "%s field value must be less than %s" % (self.key, str(self.rule.lt))

        if code == 573:
            return "%s field value must be less than or equal to %s" % (self.key, str(self.rule.lte))

        return "%s field fails the 'RangeFilter' filter check" % self.key

    def filter_required(self):
        """ 检查过滤器是否必须执行
        """
        if not self.rule.required and self.value is None:
            return False

        if self.rule.direct_type not in [int, float, Decimal, datetime.datetime]:
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
        super(RangeFilter, self).__call__()

        value = self.value if isinstance(self.value, list) else [self.value]

        # 大于
        if self.rule.gt is not None:
            rst = [not v > self.rule.gt for v in value]
            if True in rst:
                raise ParamsValueError(self.range_code_gt, filter=self)

        # 大于等于
        if self.rule.gte is not None:
            rst = [not v >= self.rule.gte for v in value]
            if True in rst:
                raise ParamsValueError(self.range_code_gte, filter=self)

        # 小于
        if self.rule.lt is not None:
            rst = [not v < self.rule.lt for v in value]
            if True in rst:
                raise ParamsValueError(self.range_code_lt, filter=self)

        # 小于等于
        if self.rule.lte is not None:
            rst = [not v <= self.rule.lte for v in value]
            if True in rst:
                raise ParamsValueError(self.range_code_lte, filter=self)

        return self.value
