# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2021
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2022/1/28 12:32 下午'
# sys
import json
import re
import socket
from datetime import (
    date,
    datetime
)
from decimal import Decimal
from json.decoder import JSONDecodeError
from urllib.parse import (
    quote,
    unquote
)
# 3p
from werkzeug.datastructures import FileStorage
# project
from .exception import ParamsValueError
from .regexp import REGEX_PARAMS
from .utils import (
    get_deep_value,
    missing
)


class BaseFilter:
    """ Base class for filter object
    """

    def __init__(self, key, value, rule):
        """
        初始化过滤器
        :param key: 参数key
        :param value: 需要过滤的值
        :param rule: 过滤的规则
        :type rule: pre_request.Rule
        """
        self.key = key
        self.value = value
        self.rule = rule

    def filter_required(self):
        """ 检查当前过滤式，是否必须要执行
        """
        return True

    def __call__(self, *args, **kwargs):
        pass


class EmptyFilter(BaseFilter):
    """ 判断参数是否为空的过滤器
    """

    def __call__(self, *args, **kwargs):
        super().__call__()

        if self.rule.required and (self.value is missing or self.value is None):
            raise ParamsValueError(f"'{self.key}' can't be empty")

        return self.value


class JsonFilter(BaseFilter):
    """ Json解析过滤器
    """

    def filter_required(self):
        """ 检查过滤器是否必须执行
        """
        if not self.rule.required and (self.value is missing or self.value is None):
            return False

        if not self.rule.json:
            return False

        if not isinstance(self.value, str):
            return False

        return True

    def __call__(self, *args, **kwargs):
        super().__call__()

        try:
            self.value = json.loads(self.value)
        except JSONDecodeError as err:
            raise ParamsValueError(f"'{self.key}' can't be parsed by json") from err

        return self.value


class SplitFilter(BaseFilter):
    """ 参数分割过滤器
    """

    def filter_required(self):
        """ 检查过滤器是否必须执行
        """
        if not self.rule.required and (self.value is missing or self.value is None):
            return False

        if self.rule.split is not None and isinstance(self.value, str):
            return True

        return False

    def __call__(self, *args, **kwargs):
        super().__call__()
        return self.value.split(self.rule.split)


class MultiFilter(BaseFilter):
    """ 处理多值的过滤器
    """

    def __call__(self, *args, **kwargs):
        super().__call__()

        if self.rule.multi and not isinstance(self.value, list):
            # empty input, and required is false
            if self.value is missing or self.value is None:
                return []

            raise ParamsValueError(f"'{self.key}' must by type of array")

        return self.value


class TypeFilter(BaseFilter):
    """ 数据类型过滤器
    """

    def filter_required(self):
        """ 检查过滤器是否必须呗执行
        """
        # Feature: Support type=None to get value directly
        if self.rule.direct_type is None:
            return False

        if not self.rule.required and (self.value is missing or self.value is None):
            return False

        if isinstance(self.value, self.rule.direct_type):
            return False

        return True

    def _type_transform(self, d_type, value):
        """ 执行类型转换
        """
        if d_type == str and isinstance(value, bytes):
            return value.decode(self.rule.encoding or "UTF-8")

        # 特殊的字符串转bool类型
        if d_type == bool and isinstance(value, str):
            return value.lower() not in {"false", "no"}

        # datetime/date convert
        if d_type in {datetime, date}:
            try:
                dt = datetime.strptime(value, self.rule.fmt)
                return dt if d_type == datetime else dt.date()
            except ValueError as err:
                raise ParamsValueError(f"'{self.key}' convert to date failed") from err

        # file don't need to convert
        if d_type == FileStorage:
            return value

        try:
            # FIX: invalid literal for int() with base 10
            # 处理int仅能转换纯数字字符串问题
            if d_type == int and isinstance(value, str) and "." in value:
                value = value.split(".")[0]

            return d_type(value)
        except (ValueError, TypeError) as err:
            raise ParamsValueError(f"'{self.key}' can't convert "
                                   f"to '{self.rule.direct_type.__name__}' type") from err

    def __call__(self, *args, **kwargs):
        super().__call__()

        if isinstance(self.value, list):
            return [self._type_transform(self.rule.direct_type, value) for value in self.value]

        return self._type_transform(self.rule.direct_type, self.value)


class TrimFilter(BaseFilter):
    """ 去除字符串前后空格的过滤器
    """

    def filter_required(self):
        """ 检查过滤器是否必须执行
        """
        if not self.rule.required and (self.value is missing or self.value is None):
            return False

        if self.rule.trim and self.rule.direct_type == str:
            return True

        return False

    def __call__(self, *args, **kwargs):
        super().__call__()

        if isinstance(self.value, str):
            return self.value.strip()

        if isinstance(self.value, list) and self.rule.multi:
            return [value.strip() for value in self.value]

        return self.value


class StringFilter(BaseFilter):
    """ 字符串处理过滤器
    """

    def filter_required(self):
        """ 验证过滤器是否必须执行
        """
        if not self.rule.required and (self.value is missing or self.value is None):
            return False

        if self.rule.direct_type != str:
            return False

        if self.rule.lower or self.rule.upper:
            return True

        return False

    def __call__(self, *args, **kwargs):
        super().__call__()

        if isinstance(self.value, str):
            return self.value.lower() if self.rule.lower else self.value.upper()

        if isinstance(self.value, list) and self.rule.multi:
            return [value.lower() if self.rule.lower else value.upper() for value in self.value]

        return self.value


class RegexpFilter(BaseFilter):
    """ 正则表达式过滤器
    """

    def filter_required(self):
        """ 检查过滤器是否必须执行
        """
        if not self.rule.required and (self.value is missing or self.value is None):
            return False

        if self.rule.direct_type != str:
            return False

        if isinstance(self.value, list) and not self.rule.multi:
            return False

        if self.rule.reg:
            return True

        for key, _ in REGEX_PARAMS.items():
            if getattr(self.rule, key) is True:
                return True

        return False

    def __call__(self, *args, **kwargs):
        super().__call__()

        # 将参数转换成数组处理
        value = self.value if isinstance(self.value, list) else [self.value]

        for v in value:
            # 判断是否符合正则
            if self.rule.reg and not re.compile(self.rule.reg, re.IGNORECASE).match(v):
                raise ParamsValueError(f"'{self.key}' does not match the regular expression")

            for key, item in REGEX_PARAMS.items():
                if not getattr(self.rule, key):
                    continue

                if not item["regex"].match(v):
                    raise ParamsValueError(item["message"] % self.key)

        return self.value


class ContentFilter(BaseFilter):
    """ 字符串内容检查过滤器
    """

    def filter_required(self):
        """ 验证过滤器是否必须执行
        """
        if not self.rule.required and (self.value is missing or self.value is None):
            return False

        if self.rule.direct_type != str:
            return False

        if isinstance(self.value, list) and not self.rule.multi:
            return False

        if self.rule.contains or self.rule.contains_any:
            return True

        if self.rule.startswith or self.rule.endswith:
            return True

        if self.rule.not_startswith or self.rule.not_endswith:
            return True

        if self.rule.excludes:
            return True

        return False

    def __call__(self, *args, **kwargs):
        super().__call__()

        value = self.value if isinstance(self.value, list) else [self.value]

        for v in value:
            if self.rule.startswith and not v.startswith(self.rule.startswith):
                raise ParamsValueError(f"'{self.key}' should start with '{self.rule.startswith}'")

            if self.rule.endswith and not v.endswith(self.rule.endswith):
                raise ParamsValueError(f"'{self.key}' should end with '{self.rule.startswith}'")

            if self.rule.not_startswith and v.startswith(self.rule.not_startswith):
                raise ParamsValueError(f"'{self.key}' should not start with '{self.rule.not_startswith}'")

            if self.rule.not_endswith and v.endswith(self.rule.not_endswith):
                raise ParamsValueError(f"'{self.key}' should not end with '{self.rule.not_endswith}'")

            for contain in self.rule.contains:
                if contain not in v:
                    raise ParamsValueError(f"'{self.key}' need required content")

            for contain in self.rule.excludes:
                if contain in v:
                    raise ParamsValueError(f"'{self.key}' contain prohibited content")

            if self.rule.contains_any:
                # check any contents
                contains_any = False
                for contain in self.rule.contains_any:
                    if contain in v:
                        contains_any = True
                        break

                if not contains_any:
                    raise ParamsValueError(f"'{self.key}' should contain special content")

        return self.value


class NetworkFilter(BaseFilter):
    """ 网络过滤器
    """

    def filter_required(self):
        """ 检查过滤器是否必须执行
        """
        if not self.rule.required and (self.value is missing or self.value is None):
            return False

        if self.rule.direct_type != str:
            return False

        if isinstance(self.value, list) and not self.rule.multi:
            return False

        if self.rule.ipv4 or self.rule.ipv6 or self.rule.mac:
            return True

        if self.rule.url_decode or self.rule.url_encode:
            return True

        return False

    @staticmethod
    def _is_ipv4(value):
        """ 判断value是否是合法的ipv4地址
        """
        try:
            socket.inet_pton(socket.AF_INET, value)
        except AttributeError:
            try:
                socket.inet_aton(value)
            except socket.error:
                return False
            return value.count(".") == 3
        except socket.error:
            return False

        return True

    @staticmethod
    def _is_ipv6(value):
        """ 判断value是否是合法的ipv6地址
        """
        try:
            socket.inet_pton(socket.AF_INET6, value)
        except socket.error:
            return False
        return True

    def __call__(self, *args, **kwargs):
        super().__call__()

        value = self.value if isinstance(self.value, list) else [self.value]

        for v in value:
            if self.rule.ipv4 and not self._is_ipv4(v):
                raise ParamsValueError(f"'{self.key}' is not a valid ipv4 address")

            if self.rule.ipv6 and not self._is_ipv6(v):
                raise ParamsValueError(f"'{self.key}' is not a valid ipv6 address")

        # url_encode or url_decode
        if self.rule.url_decode or self.rule.url_encode:
            encoding = self.rule.encoding or "UTF-8"
            if isinstance(self.value, list):
                for idx, v in enumerate(self.value):
                    self.value[idx] = unquote(v, encoding) if self.rule.url_decode else quote(v, encoding)
            else:
                self.value = unquote(self.value, encoding) if self.rule.url_decode else quote(self.value, encoding)

        return self.value


class LengthFilter(BaseFilter):
    """ 判断字符串长度的过滤器
    """

    def filter_required(self):
        """ 检查过滤器是否必须执行
        """
        if not self.rule.required and (self.value is missing or self.value is None):
            return False

        # 长度过滤器仅针对字符串、数组结构有效
        if not isinstance(self.value, (list, str)):
            return False

        if self.rule.direct_type != str:
            return False

        if self.rule.len is not None:
            return True

        if self.rule.gt is not None:
            return True

        if self.rule.gte is not None:
            return True

        if self.rule.lt is not None:
            return True

        if self.rule.lte is not None:
            return True

        return False

    def __call__(self, *args, **kwargs):
        super().__call__()

        # 数据类型为list但multi!=True时，当成整体判断长度
        for value in self.value if isinstance(self.value, list) and self.rule.multi else [self.value]:
            if self.rule.len is not None and len(value) != self.rule.len:
                raise ParamsValueError(f"the length of '{self.key}' should be equal to {self.rule.len}")

            # 大于
            if self.rule.gt is not None and not len(value) > self.rule.gt:
                raise ParamsValueError(f"the length of '{self.key}' should be greater than {self.rule.gt}")

            # 大于等于
            if self.rule.gte is not None and not len(value) >= self.rule.gte:
                raise ParamsValueError(f"the length of '{self.key}' should be greater than or equal to {self.rule.gte}")

            # 小于
            if self.rule.lt is not None and not len(value) < self.rule.lt:
                raise ParamsValueError(f"the length of '{self.key}' should be less than {self.rule.lt}")

            # 小于等于
            if self.rule.lte is not None and not len(value) <= self.rule.lte:
                raise ParamsValueError(f"the length of '{self.key}' should be less than or equal to {self.rule.lte}")

        return self.value


class RangeFilter(BaseFilter):
    """ 取值范围过滤器
    """

    def filter_required(self):
        """ 检查过滤器是否必须执行
        """
        if not self.rule.required and (self.value is missing or self.value is None):
            return False

        if isinstance(self.value, list) and not self.rule.multi:
            return False

        # 取值范围检查器，在type=list时不生效，此时将value视为一个整体
        if self.rule.direct_type not in {int, float, Decimal, datetime, date}:
            return False

        if self.rule.gt is not None:
            return True

        if self.rule.gte is not None:
            return True

        if self.rule.lt is not None:
            return True

        if self.rule.lte is not None:
            return True

        return False

    def __call__(self, *args, **kwargs):
        super().__call__()

        value = self.value if isinstance(self.value, list) else [self.value]

        # 大于
        if self.rule.gt is not None:
            rst = {not v > self.rule.gt for v in value}
            if True in rst:
                raise ParamsValueError(f"'{self.key}' should be greater than {self.rule.gt}")

        # 大于等于
        if self.rule.gte is not None:
            rst = {not v >= self.rule.gte for v in value}
            if True in rst:
                raise ParamsValueError(f"'{self.key}' should be greater than or equal to {self.rule.gte}")

        # 小于
        if self.rule.lt is not None:
            rst = {not v < self.rule.lt for v in value}
            if True in rst:
                raise ParamsValueError(f"'{self.key}' should be less than {self.rule.lt}")

        # 小于等于
        if self.rule.lte is not None:
            rst = {not v <= self.rule.lte for v in value}
            if True in rst:
                raise ParamsValueError(f"'{self.key}' should be less than or equal to {self.rule.lte}")

        return self.value


class EqualFilter(BaseFilter):
    """ 判断数值相等过滤器
    """

    def filter_required(self):
        """ 检查过滤器是否必须执行
        """
        if not self.rule.required and (self.value is missing and self.value is None):
            return False

        if isinstance(self.value, list) and not self.rule.multi:
            return False

        if self.rule.eq is not None:
            return True

        if self.rule.neq is not None:
            return True

        return False

    def __call__(self, *args, **kwargs):
        super().__call__()

        for v in self.value if isinstance(self.value, list) else [self.value]:
            if self.rule.eq is not None and v != self.rule.eq:
                raise ParamsValueError(f"'{self.key}' should be equal to '{self.rule.eq}'")

            if self.rule.neq is not None and v == self.rule.neq:
                raise ParamsValueError(f"'{self.key}' should be equal to '{self.rule.neq}'")

        return self.value


class EnumFilter(BaseFilter):
    """ 枚举过滤器
    """

    def filter_required(self):
        """ 检查过滤器是否必须执行
        """
        if not self.rule.required and self.value is missing:
            return False

        if isinstance(self.value, list) and not self.rule.multi:
            return False

        if self.rule.enum:
            return True

        return False

    def __call__(self, *args, **kwargs):
        super().__call__()

        for v in self.value if isinstance(self.value, list) else [self.value]:
            if v not in self.rule.enum:
                raise ParamsValueError(f"'{self.key}' must be one of the following '{self.rule.enum}'")

        return self.value


class DefaultFilter(BaseFilter):
    """ 填充默认值的过滤器
    """

    def __call__(self, *args, **kwargs):
        super().__call__()

        if not self.rule.required and (self.value is missing or self.value is None):
            self.value = self.rule.default

        return self.value


class RequiredWithFilter(BaseFilter):
    """ Cross struct check
    """

    def filter_required(self):
        """ 验证是否需要进行过滤
        """
        if self.rule.required_with is not None:
            return True

        return False

    def __call__(self, *args, **kwargs):
        """ 过滤器被调用时的处理
        """
        super().__call__()

        # 所有请求后的处理函数
        params = kwargs.get("params", {})

        other_v = get_deep_value(self.rule.required_with, params, None, deep=True)
        this_v = get_deep_value(self.rule.key_map or self.key, params, None, deep=True)
        if other_v is not None and this_v is None:
            raise ParamsValueError(f"'{self.key}' is required while '{self.rule.required_with}' is not empty")

        return self.value


class EqualKeyFilter(BaseFilter):
    """ Cross struct check
    """

    support_rules = {"eq_key", "neq_key", "gt_key", "gte_key", "lt_key", "lte_key"}

    def __call__(self, *args, **kwargs):
        """ 过滤器被调用时的处理
        """
        super().__call__()

        # 所有请求后的处理函数
        params = kwargs.get("params", {})
        value = get_deep_value(self.rule.key_map or self.key, params, None, deep=True)

        # BUG: complex filter value will be None
        if not self.rule.required and value == self.rule.default:
            return value

        for r_key in self.support_rules:
            other_key = getattr(self.rule, r_key, None)

            # 当前规则不需要处理
            if other_key is None:
                continue

            other_v = get_deep_value(other_key, params, None, deep=True)
            # 如果other_v是None，则说明other_key允许为空，并且用户未填写
            if other_v is None:
                continue

            if not isinstance(other_v, self.rule.direct_type):
                raise TypeError("'eq_key' 规则仅支持相同数据类型参数判断")

            if r_key == "eq_key" and value != other_v:
                raise ParamsValueError(f"'{self.key}' should be the same as '{self.rule.eq_key}'")

            if r_key == "neq_key" and value == other_v:
                raise ParamsValueError(f"'{self.key}' should be different from '{self.rule.neq_key}'")

            if r_key == "gt_key" and value <= other_v:
                raise ParamsValueError(f"'{self.key}' should be greater than '{self.rule.gt_key}'")

            if r_key == "gte_key" and value < other_v:
                raise ParamsValueError(f"'{self.key}' should be greater than or equal to '{self.rule.gte_key}'")

            if r_key == "lt_key" and value >= other_v:
                raise ParamsValueError(f"'{self.key}' should be less than '{self.rule.lt_key}'")

            if r_key == "lte_key" and value > other_v:
                raise ParamsValueError(f"'{self.key}' should be less than or equal to '{self.rule.lte_key}'")

        return value
