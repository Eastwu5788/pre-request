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
from pre_request.regexp import REGEX_PARAMS


class RegexpFilter(BaseFilter):
    """
    正则表达式过滤器
    """

    def filter_required(self):
        """ 检查过滤器是否必须执行
        """
        if not self.rule.required and (self.value is missing or self.value is None):
            return False

        if self.rule.direct_type != str:
            return False

        if isinstance(self.value, list) and not self.rule.multi:
            return False

        if self.rule.reg:
            return True

        for key, _ in REGEX_PARAMS.items():
            if getattr(self.rule, key) is True:
                return True

        return False

    def __call__(self, *args, **kwargs):
        super().__call__()

        # 将参数转换成数组处理
        value = self.value if isinstance(self.value, list) else [self.value]

        for v in value:
            # 判断是否符合正则
            if self.rule.reg and not re.compile(self.rule.reg, re.IGNORECASE).match(v):
                raise ParamsValueError(f"'{self.key}' does not match the regular expression")

            for key, item in REGEX_PARAMS.items():
                if not getattr(self.rule, key):
                    continue

                if not item["regex"].match(v):
                    raise ParamsValueError(item["message"] % self.key)

        return self.value
