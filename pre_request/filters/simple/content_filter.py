# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2020
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-04-10 16:41'
from pre_request.exception import ParamsValueError
from pre_request.filters.base import BaseFilter


class ContentFilter(BaseFilter):
    """ 字符串内容检查过滤器
    """

    not_contain_all_error = 481
    not_contain_any_error = 482

    excludes_error = 483

    startswith_error = 484
    endswith_error = 485

    def fmt_error_message(self, code):
        """ 格式化错误信息
        """
        if code == self.not_contain_all_error:
            return f"{self.key} field is missing required content"

        if code == self.not_contain_any_error:
            return f"{self.key} field must contain the specified content"

        if code == self.excludes_error:
            return f"{self.key} field contains prohibited content"

        if code == self.startswith_error:
            return f"{self.key} field must start with '{self.rule.startswith}'"

        if code == self.endswith_error:
            return f"{self.key} field must end with '{self.rule.startswith}'"

        return f"{self.key} field fails the 'ContainFilter' filter check"

    def filter_required(self):
        """ 验证过滤器是否必须执行
        """
        if not self.rule.required and self.value is None:
            return False

        if not isinstance(self.value, str):
            return False

        if self.rule.contains or self.rule.contains_any:
            return True

        if self.rule.startswith or self.rule.endswith:
            return True

        if self.rule.excludes:
            return True

        return False

    def __call__(self, *args, **kwargs):
        super().__call__()

        if self.rule.startswith and not self.value.startswith(self.rule.startswith):
            raise ParamsValueError(self.startswith_error, filter=self)

        if self.rule.endswith and not self.value.endswith(self.rule.endswith):
            raise ParamsValueError(self.endswith_error, filter=self)

        for contain in self.rule.contains:
            if contain not in self.value:
                raise ParamsValueError(self.not_contain_all_error, filter=self)

        for contain in self.rule.excludes:
            if contain in self.value:
                raise ParamsValueError(self.excludes_error, filter=self)

        for contain in self.rule.contains_any:
            if contain in self.value:
                return self.value

        if self.rule.contains_any:
            raise ParamsValueError(self.not_contain_any_error, filter=self)

        return self.value
