# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2020
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-04-10 17:09'
from pre_request.exception import ParamsValueError
from pre_request.regexp import LongitudeRegexp, LatitudeRegexp
from pre_request.filters.base import BaseFilter


class LocationFilter(BaseFilter):
    """ 地址位置过滤器
    """
    latitude_error_code = 590
    longitude_error_code = 591

    def fmt_error_message(self, code):
        """ 格式化错误信息
        """
        if code == self.latitude_error_code:
            return "%s字段不是合法的纬度!" % self.key

        if code == self.longitude_error_code:
            return "%s字段不是合法的经度!" % self.key

        return "%s字段未通过LocationFilter过滤器!" % self.key

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
        super(LocationFilter, self).__call__()

        fmt_value = self.value if isinstance(self.value, list) else [self.value]

        for value in fmt_value:
            if self.rule.longitude and not LongitudeRegexp()(value):
                raise ParamsValueError(self.longitude_error_code, filter=self)

            if self.rule.latitude and not LatitudeRegexp()(value):
                raise ParamsValueError(self.latitude_error_code, filter=self)

        return self.value
