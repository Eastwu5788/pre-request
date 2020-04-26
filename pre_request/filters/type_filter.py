# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2019
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-03-17 15:43'
from pre_request.exception import ParamsValueError
from .base import BaseFilter


_false_str_list = ["False", "false", "No", "no"]


class TypeFilter(BaseFilter):
    """
    数据类型过滤器
    """
    error_code = 562

    def fmt_error_message(self, _):
        """ 格式化错误消息
        """
        return "%s字段无法转换成(%s)类型!" % (self.key, self.rule.direct_type.__name__)

    def filter_required(self):
        """ 检查过滤器是否必须呗执行
        """
        if not self.rule.required and self.value is None:
            return False

        if isinstance(self.value, self.rule.direct_type):
            return False

        return True

    def _type_transform(self, d_type, value):
        """
        :param d_type:
        :param value:
        :return:
        """
        if d_type == str and isinstance(value, bytes):
            return value.decode('utf-8')

        # 特殊的字符串转bool类型
        if d_type == bool and isinstance(value, str):
            return value not in _false_str_list

        try:
            # FIX: invalid literal for int() with base 10
            # 处理int仅能转换纯数字字符串问题
            if d_type == int and "." in value:
                value = value.split(".")[0]

            return d_type(value)
        except ValueError:
            raise ParamsValueError(self.error_code, filter=self)

    def __call__(self, *args, **kwargs):
        super(TypeFilter, self).__call__()

        if isinstance(self.value, str):
            return self._type_transform(self.rule.direct_type, self.value)

        if isinstance(self.value, list):
            return [self._type_transform(self.rule.direct_type, value) for value in self.value]

        return self.value
