# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2019
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-03-17 15:48'
import json
from json.decoder import JSONDecodeError

from pre_request.exception import ParamsValueError
from .base import BaseFilter


class JsonFilter(BaseFilter):
    """Json解析过滤器"""

    error_code = 570

    def __call__(self, *args, **kwargs):
        super(JsonFilter, self).__call__()

        # 不需要转换成json
        if not self.rule.json_load:
            return self.value

        # 不是字符串类型，将被忽略
        if self.rule.direct_type != str:
            return self.value

        # 允许为空的情况下，不需要处理
        if self.rule.allow_empty and (self.value is None or not isinstance(self.value, str)):
            return self.value

        try:
            self.value = json.loads(self.value)
        except JSONDecodeError:
            raise ParamsValueError(self.error_code, filter=self)

        return self.value
