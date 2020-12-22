# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2019
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-03-17 15:39'


class PreRequestException(Exception):
    """ PreRequest base exception
    """


class ParamsValueError(ValueError):
    """ Invalid input params value exception
    """

    def __init__(self, code, **context):
        super().__init__()
        self.code = code
        self.context = context

    def form_message(self, fuzzy=False):  # noqa: disable
        """ format error message
        """
        message = "Parameter verification failed, please check your input"

        # 模糊错误信息
        if fuzzy:
            return message

        # read formatted message from  context
        message = self.context.get("message") or message

        # read filter object
        filter_obj = self.context.get("filter")
        if not filter_obj:
            return message

        # Read formatter message from custom filter
        filter_fmt_msg = filter_obj.fmt_error_message(self.code)
        if filter_fmt_msg is not None and isinstance(filter_fmt_msg, str):
            return filter_fmt_msg

        return message
