# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2020
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-04-10 17:09'
# sys
import socket

# project
from pre_request.regexp import MacRegexp
from pre_request.exception import ParamsValueError
from pre_request.filters.base import BaseFilter


class NetworkFilter(BaseFilter):
    """网络过滤器
    """

    ipv4_error_code = 487
    ipv6_error_code = 488
    mac_error_code = 489

    def fmt_error_message(self, code):
        """ 格式化错误消息
        """
        if code == self.ipv4_error_code:
            return "%s field does not conform to ipv4 format" % self.key

        if code == self.ipv6_error_code:
            return "%s field does not conform to ipv6 format" % self.key

        if code == self.mac_error_code:
            return "%s field is not a valid MAC address" % self.key

        return "%s field fails the 'NetworkFilter' filter check" % self.key

    def filter_required(self):
        """ 检查过滤器是否必须执行
        """
        if not self.rule.required and self.value is None:
            return False

        if self.rule.direct_type != str:
            return False

        if self.rule.ipv4 or self.rule.ipv6 or self.rule.mac:
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
        super(NetworkFilter, self).__call__()

        value = self.value if isinstance(self.value, list) else [self.value]

        for v in value:
            if self.rule.ipv4 and not self._is_ipv4(v):
                raise ParamsValueError(self.ipv4_error_code, filter=self)

            if self.rule.ipv6 and not self._is_ipv6(v):
                raise ParamsValueError(self.ipv6_error_code, filter=self)

            if self.rule.mac and not MacRegexp()(v):
                raise ParamsValueError(self.mac_error_code, filter=self)

        return self.value
