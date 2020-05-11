# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2019
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-03-17 15:38'
import re

from pre_request.exception import ParamsValueError
from pre_request.regexp import Regexp
from pre_request.filters.base import BaseFilter


class RegexpFilter(BaseFilter):
    """
    正则表达式过滤器
    """
    error_code = 566

    def fmt_error_message(self, _):
        """ 格式化错误消息
        """
        return "%s字段不符合格式要求!" % self.key

    def filter_required(self):
        """ 检查过滤器是否必须执行
        """
        if not self.rule.required and self.value is None:
            return False

        if self.rule.reg and self.rule.direct_type == str:
            return True

        return False

    def __call__(self, *args, **kwargs):
        super(RegexpFilter, self).__call__()

        # 将参数转换成数组处理
        fmt_value = self.value if isinstance(self.value, list) else [self.value]

        for value in fmt_value:
            # 判断是否符合正则
            if not Regexp(self.rule.reg, re.IGNORECASE)(value):
                raise ParamsValueError(self.error_code, filter=self)

        return self.value
