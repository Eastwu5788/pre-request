# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2019
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-03-17 15:39'


class PreRequestException(Exception):
    """ Pre-request 异常基类
    """


class ParamsValueError(ValueError):
    """自定义异常"""

    def __init__(self, code, **context):
        super().__init__()
        self.code = code
        self.context = context

    def form_message(self):  # noqa: disable
        """ 格式化JSON格式的错误消息
        """
        message = "参数检测失败，请检查您的输入!"

        # read filter object
        filter_obj = self.context["filter"]

        # Read formatter message from custom filter
        filter_fmt_msg = filter_obj.fmt_error_message(self.code)
        if filter_fmt_msg is not None and isinstance(filter_fmt_msg, str):
            return filter_fmt_msg

        return message
