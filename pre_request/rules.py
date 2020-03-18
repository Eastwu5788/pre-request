# -*- coding: utf-8 -*-

"""
该文件主要定义所有的规则处理类
"""


class Length(object):
    """
    使用Length类限定字符串长度范围
    """

    def __init__(self, min_len=None, max_len=None):
        """
        初始化字符串长度
        :param min_len: 字符串最小值，如果为0表示不加限制
        :param max_len: 字符串长度最大值，如果为0表示不加限制
        """
        self.min_len = min_len
        self.max_len = max_len

        if self.min_len is not None and self.min_len < 0:
            raise ValueError("参数'min_len'不应小于0")

        if self.max_len is not None and self.max_len < 0:
            raise ValueError("参数'max_len'不应小于0")

        if self.min_len is not None and self.max_len is not None and self.max_len < self.min_len:
            raise ValueError("字符串长度设置失败,最大长度不能小于最小长度!")

    def need_check(self):
        """是否需要进行长度校验"""
        return self.min_len is not None or self.max_len is not None

    def check_length(self, ori_str=""):
        """检查字符串长度"""
        length = len(ori_str) if ori_str else 0
        if self.min_len is not None:
            if length < self.min_len:
                return False
        if self.max_len is not None:
            if length > self.max_len:
                return False
        return True


class Range(object):
    """
    数值范围限定 仅在direct_type为float，int时生效
    """
    def __init__(self, num_min=None, num_max=None):
        """
        数字范围限定
        :param num_min: 最小值，如果为-1表示不加限制
        :param num_max: 最大值，如果为-1表示不加限制
        """
        self.num_min = num_min
        self.num_max = num_max
        if self.num_min is not None and self.num_max is not None and self.num_max < self.num_min:
            raise ValueError("范围限定设置失败,最大值不能小于最小值!")

    def need_check(self):
        """是否需要进行长度校验"""
        return self.num_min is not None or self.num_max is not None

    def check_range(self, ori_num):
        """检查字符串长度"""
        if self.num_min is not None:
            if ori_num < self.num_min:
                return False
        if self.num_max is not None:
            if ori_num > self.num_max:
                return False
        return True


class Rule(object):  # pylint: disable=too-many-instance-attributes
    """
    字段遵守的规则定义类
    """
    def __init__(self, **kwargs):
        # 字段目标数据类型
        self.direct_type = kwargs.get("direct_type", str)

        # 当前字段是否允许为空
        self.allow_empty = kwargs.get("allow_empty", False)
        # 当前字段默认值，如果不允许为空，则次字段无意义
        self.default = kwargs.get("default", None)
        # 去除前后的空格
        self.trim = kwargs.get("trim", False)

        # 字段枚举值设置
        self.enum = kwargs.get("enum", list())
        # range,整数范围限定, 只在direct_type为数字时有效
        self.range = kwargs.get("range", Range())

        # 正则表达式
        self.reg = kwargs.get("reg", None)
        # Email判断
        self.email = kwargs.get("email", False)
        # 手机号判断
        self.mobile = kwargs.get("mobile", False)

        # 字符串长度判断
        self.len = kwargs.get("length", Length())

        # key映射
        self.key_map = kwargs.get("key_map", None)

        # 是否需要进行json解析
        self.json_load = kwargs.get("json", False)

        # 自定义处理callback, 在所有的filter处理完成后，通过callback回调给用户进行自定义处理
        self.callback = kwargs.get("callback", None)
