# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2019
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-03-17 15:38'
# sys
import re
# project
from pre_request.exception import ParamsValueError
from pre_request.filters.base import BaseFilter
from pre_request.utils import missing


class RegexpFilter(BaseFilter):
    """
    正则表达式过滤器
    """

    def filter_required(self):
        """ 检查过滤器是否必须执行
        """
        if not self.rule.required and (self.value is missing or self.value is None):
            return False

        if self.rule.reg and self.rule.direct_type == str:
            return True

        return False

    def __call__(self, *args, **kwargs):
        super().__call__()

        # 将参数转换成数组处理
        fmt_value = self.value if isinstance(self.value, list) else [self.value]

        for value in fmt_value:
            # 判断是否符合正则
            if not re.compile(self.rule.reg, re.IGNORECASE).match(value):
                raise ParamsValueError(f"{self.key} field does not confirm to regular expression")

        return self.value
