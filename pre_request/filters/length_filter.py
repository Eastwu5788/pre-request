# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2019
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-03-17 15:37'
from pre_request.exception import ParamsValueError
from .base import BaseFilter


class LengthFilter(BaseFilter):
    """
    判断字符串长度的过滤器
    """

    length_code_gt = 574
    length_code_gte = 575
    length_code_lt = 576
    length_code_lte = 577

    def fmt_error_message(self, code):
        """ 格式化错误消息
        """
        if code == 574:
            return "%s字段长度必须大于%s!" % (self.key, str(self.rule.gt))

        if code == 575:
            return "%s字段长度必须大于等于%s!" % (self.key, str(self.rule.gte))

        if code == 576:
            return "%s字段长度必须小于%s!" % (self.key, str(self.rule.lt))

        if code == 577:
            return "%s字段长度必须小于等于%s!" % (self.key, str(self.rule.lte))

        return "%s字段未通过'LengthFilter'过滤器检查!" % self.key

    def __call__(self, *args, **kwargs):
        super(LengthFilter, self).__call__()

        # None值不做处理
        if self.rule.allow_empty and self.value is None:
            return self.value

        if self.rule.direct_type not in [str, list, set, tuple]:
            return self.value

        # 大于
        if self.rule.gt is not None and not len(self.value) > self.rule.gt:
            raise ParamsValueError(self.length_code_gt, filter=self)

        # 大于等于
        if self.rule.gte is not None and not len(self.value) >= self.rule.gte:
            raise ParamsValueError(self.length_code_gte, filter=self)

        # 小于
        if self.rule.lt is not None and not len(self.value) < self.rule.lt:
            raise ParamsValueError(self.length_code_lt, filter=self)

        # 小于等于
        if self.rule.lte is not None and not len(self.value) <= self.rule.lte:
            raise ParamsValueError(self.length_code_lte, filter=self)

        return self.value
