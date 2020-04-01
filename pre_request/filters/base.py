# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2019
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-03-17 15:34'


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
