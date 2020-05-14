# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2019
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-03-17 15:34'


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

    def fmt_error_message(self, code):  # pylint: disable=unused-argument
        """ 返回格式化的错误消息
        """
        return None

    def __call__(self, *args, **kwargs):
        pass
