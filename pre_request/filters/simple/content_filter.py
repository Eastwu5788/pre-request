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
    not_contain_all_error = 581
    not_contain_any_error = 582

    excludes_error = 583

    startswith_error = 584
    endswith_error = 585

    def fmt_error_message(self, code):
        """ 格式化错误信息
        """
        if code == self.not_contain_all_error:
            return "%s字段缺少必要内容" % self.key

        if code == self.not_contain_any_error:
            return "%s字段未包含指定内容" % self.key

        if code == self.excludes_error:
            return "%s字段未包含禁止内容" % self.key

        if code == self.startswith_error:
            return "%s字段必须以'%s'开头" % (self.key, self.rule.startswith)

        if code == self.endswith_error:
            return "%s字段必须以'%s'结尾" % (self.key, self.rule.startswith)

        return "%s字段未通过ContainFilter过滤器检查" % self.key

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
        super(ContentFilter, self).__call__()

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
