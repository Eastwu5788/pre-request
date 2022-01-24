# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2020
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-04-10 16:41'
from pre_request.exception import ParamsValueError
from pre_request.filters.base import BaseFilter
from pre_request.utils import missing


class ContentFilter(BaseFilter):
    """ 字符串内容检查过滤器
    """

    def filter_required(self):
        """ 验证过滤器是否必须执行
        """
        if not self.rule.required and (self.value is missing or self.value is None):
            return False

        if self.rule.direct_type != str or not isinstance(self.value, (str, list)):
            return False

        if self.rule.contains or self.rule.contains_any:
            return True

        if self.rule.startswith or self.rule.endswith:
            return True

        if self.rule.not_startswith or self.rule.not_endswith:
            return True

        if self.rule.excludes:
            return True

        return False

    def __call__(self, *args, **kwargs):
        super().__call__()

        value = self.value if isinstance(self.value, list) else [self.value]

        for v in value:
            if self.rule.startswith and not v.startswith(self.rule.startswith):
                raise ParamsValueError(f"'{self.key}' should start with '{self.rule.startswith}'")

            if self.rule.endswith and not v.endswith(self.rule.endswith):
                raise ParamsValueError(f"'{self.key}' should end with '{self.rule.startswith}'")

            if self.rule.not_startswith and v.startswith(self.rule.not_startswith):
                raise ParamsValueError(f"'{self.key}' should not start with '{self.rule.not_startswith}'")

            if self.rule.not_endswith and v.endswith(self.rule.not_endswith):
                raise ParamsValueError(f"'{self.key}' should not end with '{self.rule.not_endswith}'")

            for contain in self.rule.contains:
                if contain not in v:
                    raise ParamsValueError(f"'{self.key}' need required content")

            for contain in self.rule.excludes:
                if contain in v:
                    raise ParamsValueError(f"'{self.key}' contain prohibited content")

            if self.rule.contains_any:
                # check any contents
                contains_any = False
                for contain in self.rule.contains_any:
                    if contain in v:
                        contains_any = True
                        break

                if not contains_any:
                    raise ParamsValueError(f"'{self.key}' should contain special content")

        return self.value
