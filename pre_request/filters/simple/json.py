# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2019
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-03-17 15:48'
# sys
import json
from json.decoder import JSONDecodeError
# project
from pre_request.exception import ParamsValueError
from pre_request.filters.base import BaseFilter
from pre_request.utils import missing


class JsonFilter(BaseFilter):
    """Json解析过滤器"""

    def filter_required(self):
        """ 检查过滤器是否必须执行
        """
        if not self.rule.required and (self.value is missing or self.value is None):
            return False

        if not self.rule.json_load:
            return False

        if not isinstance(self.value, str):
            return False

        return True

    def __call__(self, *args, **kwargs):
        super().__call__()

        try:
            self.value = json.loads(self.value)
        except JSONDecodeError as err:
            raise ParamsValueError(f"{self.key} field cannot be parsed by json") from err

        return self.value
