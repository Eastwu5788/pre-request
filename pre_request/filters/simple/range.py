# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2019
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-03-17 15:45'
# sys
from datetime import (
    date,
    datetime
)
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

        # 取值范围检查器，在type=list时不生效，此时将value视为一个整体
        if self.rule.direct_type not in {int, float, Decimal, datetime, date}:
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
                raise ParamsValueError(f"'{self.key}' should be greater than {self.rule.gt}")

        # 大于等于
        if self.rule.gte is not None:
            rst = [not v >= self.rule.gte for v in value]
            if True in rst:
                raise ParamsValueError(f"'{self.key}' should be greater than or equal to {self.rule.gte}")

        # 小于
        if self.rule.lt is not None:
            rst = [not v < self.rule.lt for v in value]
            if True in rst:
                raise ParamsValueError(f"'{self.key}' should be less than {self.rule.lt}")

        # 小于等于
        if self.rule.lte is not None:
            rst = [not v <= self.rule.lte for v in value]
            if True in rst:
                raise ParamsValueError(f"'{self.key}' should be less than or equal to {self.rule.lte}")

        return self.value
