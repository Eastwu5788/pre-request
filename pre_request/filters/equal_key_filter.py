# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2020
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-04-13 09:16'
from pre_request.exception import ParamsValueError
from .base import BaseFilter


class EqualKeyFilter(BaseFilter):

    eq_key_error = 593

    def fmt_error_message(self, code):
        """ 格式化错误消息

        :param code: 错误码
        """
        if code == self.eq_key_error:
            return "'%s'与'%s'值必须相同" % (self.key, self.rule.eq_key)

        return "过滤器'EqualKeyFilter'过滤器检查'%s'参数失败" % self.key

    def filter_required(self):
        """ 验证是否需要进行过滤
        """
        if not self.rule.required and self.value is None:
            return False

        if self.rule.eq_key is not None or self.rule.neq_key is not None:
            return True

        return False

    def __call__(self, *args, **kwargs):
        """ 过滤器被调用时的处理
        """
        super(EqualKeyFilter, self).__call__()

        # 所有请求后的处理函数
        params = kwargs.get("params", dict())

        if self.rule.eq_key is not None:
            other_v = params.get(self.rule.eq_key, None)

            # 无法对不同数据类型进行判断
            if other_v is not None and isinstance(other_v, self.rule.direct_type):
                raise TypeError("'eq_key' 参数仅支持相同数据类型参数判断")

            # other_v 为None值表示为默认值，无需进行判断
            if other_v is not None and self.value != other_v:
                raise ParamsValueError(self.eq_key_error, filter=self)

        return self.value
