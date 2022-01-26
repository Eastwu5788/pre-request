# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2019
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-03-17 15:43'
# sys
from datetime import (
    date,
    datetime
)
# 3p
from werkzeug.datastructures import FileStorage
# project
from pre_request.exception import ParamsValueError
from pre_request.filters.base import BaseFilter
from pre_request.utils import missing


_false_str_list = {"false", "no"}


class TypeFilter(BaseFilter):
    """
    数据类型过滤器
    """

    def filter_required(self):
        """ 检查过滤器是否必须呗执行
        """
        # Feature: Support type=None to get value directly
        if self.rule.direct_type is None:
            return False

        if not self.rule.required and (self.value is missing or self.value is None):
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
            return value.decode(self.rule.encoding or "UTF-8")

        # 特殊的字符串转bool类型
        if d_type == bool and isinstance(value, str):
            return value.lower() not in _false_str_list

        # datetime/date convert
        if d_type in {datetime, date}:
            try:
                dt = datetime.strptime(value, self.rule.fmt)
                return dt if d_type == datetime else dt.date()
            except ValueError as err:
                raise ParamsValueError(f"'{self.key}' convert to date failed") from err

        # file don't need to convert
        if d_type == FileStorage:
            return value

        try:
            # FIX: invalid literal for int() with base 10
            # 处理int仅能转换纯数字字符串问题
            if d_type == int and isinstance(value, str) and "." in value:
                value = value.split(".")[0]

            return d_type(value)
        except (ValueError, TypeError) as err:
            raise ParamsValueError(f"'{self.key}' can't convert "
                                   f"to '{self.rule.direct_type.__name__}' type") from err

    def __call__(self, *args, **kwargs):
        super().__call__()

        if isinstance(self.value, list):
            return [self._type_transform(self.rule.direct_type, value) for value in self.value]

        return self._type_transform(self.rule.direct_type, self.value)
