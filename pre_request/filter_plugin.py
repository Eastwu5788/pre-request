# -*- coding: utf-8 -*-

import re
import json
from json.decoder import JSONDecodeError

from .filter_rules import Rule
from .filter_error import ParamsValueError

_false_str_list = ["False", "false", "No", "no", "0", "None", "", "[]", "()", "{}", "0.0"]


class BaseFilter(object):
    """
    过滤器基类
    """
    # 错误码
    error_code = 500

    def __init__(self, key, value, rule):
        """
        初始化过滤器
        :param key: 参数key
        :param value: 需要过滤的值
        :param rule: 过滤的规则
        :type rule: Rule
        """
        self.key = key
        self.value = value
        self.rule = rule

    def __call__(self):
        pass


class EmptyFilter(BaseFilter):
    """
    判断参数是否为空的过滤器
    """
    error_code = 560

    def __call__(self, *args, **kwargs):
        super(EmptyFilter, self).__call__()

        # 参数输入值为空
        if not self.value:
            if self.rule.allow_empty:
                self.value = self.rule.default
            else:
                raise ParamsValueError(self.error_code, filter=self)
        return self.value


class TrimFilter(BaseFilter):
    """
    去除字符串前后空格的过滤器
    """
    error_code = 569

    def __call__(self, *args, **kwargs):
        super(TrimFilter, self).__call__()

        if self.rule.trim and isinstance(self.value, str):
            return self.value.strip()
        else:
            return self.value


class LengthFilter(BaseFilter):
    """
    判断字符串长度的过滤器
    """
    error_code = 561

    def __call__(self, *args, **kwargs):
        super(LengthFilter, self).__call__()

        if self.rule.len and self.rule.len.need_check():
            if self.rule.allow_empty and not self.value:
                return self.value
            if not self.rule.len.check_length(self.value):
                raise ParamsValueError(self.error_code, filter=self)
        return self.value


class RegexpFilter(BaseFilter):
    """
    正则表达式过滤器
    """
    error_code = 566

    def __call__(self, *args, **kwargs):
        super(RegexpFilter, self).__call__()

        # 判断是否需要进行正则匹配
        if self.rule.reg and isinstance(self.rule.reg, str):
            # 判断是否符合正则
            from .filter_regexp import Regexp
            if not Regexp(self.rule.reg, re.IGNORECASE)(self.value):
                raise ParamsValueError(self.error_code, filter=self)
        return self.value


class TypeFilter(BaseFilter):
    """
    数据类型过滤器
    """
    error_code = 562

    def __call__(self, *args, **kwargs):
        super(TypeFilter, self).__call__()

        direct_type = self.rule.direct_type

        # 初始类型就是字符串，并且默认是安全的，则不需要处理
        if isinstance(self.value, direct_type):
            return self.value

        if direct_type == str:
            if self.rule.allow_empty and not self.value:
                return self.value

            if isinstance(self.value, bytes):
                self.value = self.value.decode('utf-8')
            return self.value
        # 特殊的字符串转bool类型
        elif direct_type == bool and self.value in _false_str_list:
            return False
        else:
            try:
                return self.rule.direct_type(self.value)
            except ValueError:
                raise ParamsValueError(self.error_code, filter=self)


class EnumFilter(BaseFilter):
    """枚举过滤器"""
    error_code = 563

    def __call__(self, *args, **kwargs):
        super(EnumFilter, self).__call__()

        if self.rule.enum and self.value not in self.rule.enum:
            raise ParamsValueError(self.error_code, filter=self)

        return self.value


class RangeFilter(BaseFilter):
    """取值范围过滤器"""
    error_code = 567
    range_code = 568

    def __call__(self, *args, **kwargs):
        super(RangeFilter, self).__call__()

        if self.rule.range.need_check():
            try:
                if not self.rule.range.check_range(self.value):
                    raise ParamsValueError(self.error_code, filter=self)
            except TypeError:
                raise ParamsValueError(self.range_code, filter=self)

        return self.value


class EmailFilter(BaseFilter):
    """邮箱过滤器"""
    error_code = 564

    def __call__(self, *args, **kwargs):
        super(EmailFilter, self).__call__()

        if self.rule.email:
            from .filter_regexp import EmailRegexp
            if not EmailRegexp()(self.value):
                raise ParamsValueError(self.error_code, filter=self)

        return self.value


class MobileFilter(BaseFilter):
    """手机号过滤器"""
    error_code = 565

    def __call__(self, *args, **kwargs):
        super(MobileFilter, self).__call__()

        if self.rule.mobile:
            from .filter_regexp import MobileRegexp
            if not MobileRegexp()(self.value):
                raise ParamsValueError(self.error_code, filter=self)

        return self.value


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
