# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2020
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-04-13 10:39'
from pre_request.exception import ParamsValueError
from pre_request.utils import get_deep_value
from pre_request.filters.base import BaseFilter


class RequiredWithFilter(BaseFilter):

    def filter_required(self):
        """ 验证是否需要进行过滤
        """
        if self.rule.required_with is not None:
            return True

        return False

    def __call__(self, *args, **kwargs):
        """ 过滤器被调用时的处理
        """
        super().__call__()

        # 所有请求后的处理函数
        params = kwargs.get("params", {})

        other_v = get_deep_value(self.rule.required_with, params, None, deep=True)

        if other_v is not None and get_deep_value(self.rule.key_map or self.key, params, None, deep=True) is None:
            raise ParamsValueError(f"when filling in the value of '{self.rule.required_with}', "
                                   f"the value of `{self.key}` must also be filled in")

        return self.value
