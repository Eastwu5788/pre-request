# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2020
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-04-13 09:16'
from pre_request.exception import ParamsValueError
from pre_request.utils import (
    get_deep_value
)
from pre_request.filters.base import BaseFilter


class EqualKeyFilter(BaseFilter):

    support_rules = ["eq_key", "neq_key", "gt_key", "gte_key", "lt_key", "lte_key"]

    def __call__(self, *args, **kwargs):
        """ 过滤器被调用时的处理
        """
        super().__call__()

        # 所有请求后的处理函数
        params = kwargs.get("params", {})
        value = get_deep_value(self.rule.key_map or self.key, params, None, deep=True)

        # BUG: complex filter value will be None
        if not self.rule.required and value == self.rule.default:
            return value

        for r_key in self.support_rules:
            other_key = getattr(self.rule, r_key, None)

            # 当前规则不需要处理
            if other_key is None:
                continue

            other_v = get_deep_value(other_key, params, None, deep=True)
            # 如果other_v是None，则说明other_key允许为空，并且用户未填写
            if other_v is None:
                continue

            if not isinstance(other_v, self.rule.direct_type):
                raise TypeError("'eq_key' 规则仅支持相同数据类型参数判断")

            if r_key == "eq_key" and value != other_v:
                raise ParamsValueError(f"'{self.key}' should be the same as '{self.rule.eq_key}'")

            if r_key == "neq_key" and value == other_v:
                raise ParamsValueError(f"'{self.key}' should be different from '{self.rule.neq_key}'")

            if r_key == "gt_key" and value <= other_v:
                raise ParamsValueError(f"'{self.key}' should be greater than '{self.rule.gt_key}'")

            if r_key == "gte_key" and value < other_v:
                raise ParamsValueError(f"'{self.key}' should be greater than or equal to '{self.rule.gte_key}'")

            if r_key == "lt_key" and value >= other_v:
                raise ParamsValueError(f"'{self.key}' should be less than '{self.rule.lt_key}'")

            if r_key == "lte_key" and value > other_v:
                raise ParamsValueError(f"'{self.key}' should be less than or equal to '{self.rule.lte_key}'")

        return value
