# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2020
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-04-13 09:16'
from pre_request.exception import ParamsValueError
from pre_request.utils import get_deep_value
from pre_request.filters.base import BaseFilter


class EqualKeyFilter(BaseFilter):

    support_rules = {
        "eq_key": 593,
        "neq_key": 594,
        "gt_key": 595,
        "gte_key": 596,
        "lt_key": 597,
        "lte_key": 598,
    }

    def fmt_error_message(self, code):
        """ 格式化错误消息

        :param code: 错误码
        """
        if code == 593:
            return "'%s'与'%s'值必须相同" % (self.key, self.rule.eq_key)

        if code == 594:
            return "'%s'与'%s'值不允许相同" % (self.key, self.rule.neq_key)

        if code == 595:
            return "'%s'应该大于'%s'" % (self.key, self.rule.gt_key)

        if code == 596:
            return "'%s'应该大于等于'%s'" % (self.key, self.rule.gte_key)

        if code == 597:
            return "'%s'应该小于'%s'" % (self.key, self.rule.lt_key)

        if code == 598:
            return "'%s'应该小于等于'%s'" % (self.key, self.rule.lte_key)

        return "过滤器'EqualKeyFilter'过滤器检查'%s'参数失败" % self.key

    def filter_required(self):
        """ 验证是否需要进行过滤
        """
        if self.rule.eq_key is not None or self.rule.neq_key is not None:
            return True

        if self.rule.gt_key is not None or self.rule.gte_key is not None:
            return True

        if self.rule.lt_key is not None or self.rule.lte_key is not None:
            return True

        return False

    def __call__(self, *args, **kwargs):
        """ 过滤器被调用时的处理
        """
        super(EqualKeyFilter, self).__call__()

        # 所有请求后的处理函数
        params = kwargs.get("params", dict())
        value = get_deep_value(self.rule.key_map or self.key, params, None, deep=True)

        # BUG: complex filter value will be None
        if not self.rule.required and value is None:
            return value

        for r_key, r_code in self.support_rules.items():
            rule = getattr(self.rule, r_key, None)

            # 当前规则不需要处理
            if rule is None:
                continue

            other_v = get_deep_value(rule, params, None, deep=True)

            if not isinstance(other_v, self.rule.direct_type):
                raise TypeError("'eq_key' 规则仅支持相同数据类型参数判断")

            if r_key == "eq_key" and value != other_v:
                raise ParamsValueError(r_code, filter=self)

            if r_key == "neq_key" and value == other_v:
                raise ParamsValueError(r_code, filter=self)

            if r_key == "gt_key" and value <= other_v:
                raise ParamsValueError(r_code, filter=self)

            if r_key == "gte_key" and value < other_v:
                raise ParamsValueError(r_code, filter=self)

            if r_key == "lt_key" and value >= other_v:
                raise ParamsValueError(r_code, filter=self)

            if r_key == "lte_key" and value > other_v:
                raise ParamsValueError(r_code, filter=self)

        return value
