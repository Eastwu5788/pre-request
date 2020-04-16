# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2019
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-03-17 15:47'
from pre_request.regexp import MobileRegexp
from pre_request.exception import ParamsValueError
from .base import BaseFilter


class MobileFilter(BaseFilter):
    """手机号过滤器"""
    error_code = 565

    def fmt_error_message(self, _):
        """ 格式化错误消息
        """
        return "%s字段不符合手机号格式!" % self.key

    def filter_required(self):
        """ 检查过滤器是否必须执行
        """
        if not self.rule.required and self.value is None:
            return False

        if not self.rule.mobile:
            return False

        return True

    def __call__(self, *args, **kwargs):
        super(MobileFilter, self).__call__()

        if not MobileRegexp()(self.value):
            raise ParamsValueError(self.error_code, filter=self)

        return self.value
