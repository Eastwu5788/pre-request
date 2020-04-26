# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2019
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-03-17 15:38'
import re

from pre_request.exception import ParamsValueError
from pre_request.regexp import Regexp
from .base import BaseFilter


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

        # 非字符串不处理正则
        if not isinstance(self.value, str):
            return False

        if self.rule.reg is not None:
            return True

        return False

    def __call__(self, *args, **kwargs):
        super(RegexpFilter, self).__call__()

        # 判断是否符合正则
        if not Regexp(self.rule.reg, re.IGNORECASE)(self.value):
            raise ParamsValueError(self.error_code, filter=self)

        return self.value
