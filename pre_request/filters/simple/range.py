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
from pre_request.utils import missing


class RangeFilter(BaseFilter):
    """取值范围过滤器"""

    def filter_required(self):
        """ 检查过滤器是否必须执行
        """
        if not self.rule.required and (self.value is missing or self.value is None):
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
        super().__call__()

        value = self.value if isinstance(self.value, list) else [self.value]

        # 大于
        if self.rule.gt is not None:
            rst = [not v > self.rule.gt for v in value]
            if True in rst:
                raise ParamsValueError(f"{self.key} field value must be greater than {str(self.rule.gt)}")

        # 大于等于
        if self.rule.gte is not None:
            rst = [not v >= self.rule.gte for v in value]
            if True in rst:
                raise ParamsValueError(f"{self.key} field value must be greater than or equal to {str(self.rule.gte)}")

        # 小于
        if self.rule.lt is not None:
            rst = [not v < self.rule.lt for v in value]
            if True in rst:
                raise ParamsValueError(f"{self.key} field value must be less than {str(self.rule.lt)}")

        # 小于等于
        if self.rule.lte is not None:
            rst = [not v <= self.rule.lte for v in value]
            if True in rst:
                raise ParamsValueError(f"{self.key} field value must be less than or equal to {str(self.rule.lte)}")

        return self.value
