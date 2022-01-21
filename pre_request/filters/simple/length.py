# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2019
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-03-17 15:37'
from pre_request.exception import ParamsValueError
from pre_request.filters.base import BaseFilter
from pre_request.utils import missing


class LengthFilter(BaseFilter):
    """
    判断字符串长度的过滤器
    """

    def filter_required(self):
        """ 检查过滤器是否必须执行
        """
        if not self.rule.required and (self.value is missing or self.value is None):
            return False

        # Value的类型是list时将其作为一个整体进行考虑
        if self.rule.direct_type == list:
            return True

        # 长度校验近对字符串、数组生效
        if self.rule.direct_type != str:
            return False

        # 排除子结构中的字符串
        if self.rule.direct_type == str and isinstance(self.value, list):
            return False

        if self.rule.len is not None:
            return True

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
            if self.rule.len is not None and len(value) != self.rule.len:
                raise ParamsValueError(f"the length of '{self.key}' should be equal to {self.rule.len}")

            # 大于
            if self.rule.gt is not None and not len(value) > self.rule.gt:
                raise ParamsValueError(f"the length of '{self.key}' should be greater than {self.rule.gt}")

            # 大于等于
            if self.rule.gte is not None and not len(value) >= self.rule.gte:
                raise ParamsValueError(f"the length of '{self.key}' should be greater than or equal to {self.rule.gte}")

            # 小于
            if self.rule.lt is not None and not len(value) < self.rule.lt:
                raise ParamsValueError(f"the length of '{self.key}' should be less than {self.rule.lt}")

            # 小于等于
            if self.rule.lte is not None and not len(value) <= self.rule.lte:
                raise ParamsValueError(f"the length of '{self.key}' should be less than or equal to {self.rule.lte}")

        return self.value
