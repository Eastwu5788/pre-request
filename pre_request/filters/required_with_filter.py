# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2020
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-04-13 10:39'
from pre_request.exception import ParamsValueError
from .base import BaseFilter


class RequiredWithFilter(BaseFilter):

    required_with_error = 599

    def fmt_error_message(self, code):
        """ 格式化错误消息

        :param code: 错误码
        """
        if code == self.required_with_error:
            return "'%s'参数填写时，当前参数`%s`也必须填写" % (self.rule.required_with, self.key)

        return "过滤器'RequiredWithFilter'过滤器检查'%s'参数失败" % self.key

    def filter_required(self):
        """ 验证是否需要进行过滤
        """
        if self.rule.required_with is not None:
            return True

        return False

    def __call__(self, *args, **kwargs):
        """ 过滤器被调用时的处理
        """
        super(RequiredWithFilter, self).__call__()

        # 所有请求后的处理函数
        params = kwargs.get("params", dict())

        other_v = params.get(self.rule.required_with, None)

        if other_v is not None and params.get(self.key) is None:
            raise ParamsValueError(self.required_with_error, filter=self)

        return self.value
