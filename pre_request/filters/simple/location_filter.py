# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2020
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-04-10 17:09'
from pre_request.exception import ParamsValueError
from pre_request.regexp import (
    latitude_regex,
    longitude_regex
)
from pre_request.filters.base import BaseFilter


class LocationFilter(BaseFilter):
    """ 地址位置过滤器
    """

    def filter_required(self):
        """ 验证过滤器是否必须执行
        """
        if not self.rule.required and self.value is None:
            return False

        if self.rule.direct_type != str:
            return False

        if self.rule.latitude or self.rule.longitude:
            return True

        return False

    def __call__(self, *args, **kwargs):
        super().__call__()

        fmt_value = self.value if isinstance(self.value, list) else [self.value]

        for value in fmt_value:
            if self.rule.longitude and not longitude_regex.match(value):
                raise ParamsValueError(f"{self.key} field does not confirm to longitude format")

            if self.rule.latitude and not latitude_regex.match(value):
                raise ParamsValueError(f"{self.key} field does not confirm to latitude format")

        return self.value
