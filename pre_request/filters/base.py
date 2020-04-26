# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2019
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-03-17 15:34'


class BaseFilter:
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

    @staticmethod
    def get_deep_key(key, params, default=None):
        """ 获取多层嵌套的参数值

        :param key: 多层次的key
        :param params: 读取的数据源
        :param default: 默认值
        """
        if key is None:
            return None

        for k in key.split("."):
            params = params.get(k, default)
            if not isinstance(params, dict) and not key.endswith(k):
                raise ValueError("Can't read deep value from path: '%s'" % key)

        return params

    def __call__(self, *args, **kwargs):
        pass
