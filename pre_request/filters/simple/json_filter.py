# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2019
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-03-17 15:48'
import json
from json.decoder import JSONDecodeError

from pre_request.exception import ParamsValueError
from pre_request.filters.base import BaseFilter


class JsonFilter(BaseFilter):
    """Json解析过滤器"""

    error_code = 570

    def fmt_error_message(self, _):
        """ 格式化错误信息

        :param _: 错误码
        """
        return "%s字段无法通过json进行解析" % self.key

    def filter_required(self):
        """ 检查过滤器是否必须执行
        """
        if not self.rule.required and self.value is None:
            return False

        if not self.rule.json_load:
            return False

        if not isinstance(self.value, str):
            return False

        return True

    def __call__(self, *args, **kwargs):
        super(JsonFilter, self).__call__()

        try:
            self.value = json.loads(self.value)
        except JSONDecodeError:
            raise ParamsValueError(self.error_code, filter=self)

        return self.value
