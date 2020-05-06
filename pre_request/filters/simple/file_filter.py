# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2020
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-04-10 17:09'
from pre_request.exception import ParamsValueError
from pre_request.regexp import FileRegexp
from pre_request.filters.base import BaseFilter


class FileFilter(BaseFilter):
    """文件过滤器"""

    error_code = 586

    def fmt_error_message(self, _):
        """ 格式化错误信息
        """
        return "%s字段不符合文件格式!" % self.key

    def filter_required(self):
        """ 验证过滤器是否必须执行
        """
        if not self.rule.required and self.value is None:
            return False

        if self.rule.file and self.rule.direct_type == str:
            return True

        return False

    def __call__(self, *args, **kwargs):
        super(FileFilter, self).__call__()

        if not FileRegexp()(self.value):
            raise ParamsValueError(self.error_code, filter=self)

        return self.value
