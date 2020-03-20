# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2019
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-03-17 15:43'
from pre_request.exception import ParamsValueError
from .base import BaseFilter


_false_str_list = ["False", "false", "No", "no", "0", "None", "", "[]", "()", "{}", "0.0"]


class TypeFilter(BaseFilter):
    """
    数据类型过滤器
    """
    error_code = 562

    def __call__(self, *args, **kwargs):
        super(TypeFilter, self).__call__()

        direct_type = self.rule.direct_type

        # 初始类型就是字符串，并且默认是安全的，则不需要处理
        if isinstance(self.value, direct_type):
            return self.value

        if direct_type == str:
            if self.rule.allow_empty and not self.value:
                return self.value

            if isinstance(self.value, bytes):
                self.value = self.value.decode('utf-8')
            return self.value

        # 特殊的字符串转bool类型
        if direct_type == bool and self.value in _false_str_list:
            return False

        try:
            # FIX: invalid literal for int() with base 10
            # 处理int仅能转换纯数字字符串问题
            if self.rule.direct_type == int and "." in self.value:
                self.value = self.value.split(".")[0]

            return self.rule.direct_type(self.value)
        except ValueError:
            raise ParamsValueError(self.error_code, filter=self)
