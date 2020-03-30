# -*- coding: utf-8 -*-

"""
该文件主要定义所有的规则处理类
"""


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

        # 正则表达式
        self.reg = kwargs.get("reg", None)
        # Email判断
        self.email = kwargs.get("email", False)
        # 手机号判断
        self.mobile = kwargs.get("mobile", False)

        # 等于
        self.eq = kwargs.get("eq", None)
        # 不等于
        self.neq = kwargs.get("neq", None)

        # 范围限定 direct_type 为数字时限定数字大小，为字符串时限定字符串长度
        # 大于
        self.gt = kwargs.get("gt", None)
        # 大于等于
        self.gte = kwargs.get("gte", None)
        # 小于
        self.lt = kwargs.get("lt", None)
        # 小于等于
        self.lte = kwargs.get("lte", None)

        # key映射
        self.key_map = kwargs.get("key_map", None)

        # 是否需要进行json解析
        self.json_load = kwargs.get("json", False)

        # 自定义处理callback, 在所有的filter处理完成后，通过callback回调给用户进行自定义处理
        self.callback = kwargs.get("callback", None)

    @property
    def gt(self):
        """ 将`gt`属性变更为动态属性
        """
        return self._gt

    @gt.setter
    def gt(self, value):
        """ Add input value type check

        :param value: User input gt value
        """
        # Ignore None
        if value is None:
            self._gt = value
            return

        # check input value type
        if not isinstance(value, int) and not isinstance(value, float):
            raise TypeError("property `gt` must be type of int or float")

        self._gt = value

    @property
    def gte(self):
        """ 将`gte`属性变更为动态属性
        """
        return self._gte

    @gte.setter
    def gte(self, value):
        """ Add input value type check

        :param value: User input gte value
        """
        # Ignore None
        if value is None:
            self._gte = value
            return

        # check input value type
        if not isinstance(value, int) and not isinstance(value, float):
            raise TypeError("property `gte` must be type of int or float")

        self._gte = value

    @property
    def lt(self):
        """ 将`lt`属性变更为动态属性
        """
        return self._lt

    @lt.setter
    def lt(self, value):
        """ Add input value type check

        :param value: User input lt value
        """
        # Ignore None
        if value is None:
            self._lt = value
            return

        # check input value type
        if not isinstance(value, int) and not isinstance(value, float):
            raise TypeError("property `lt` must be type of int or float")

        self._lt = value

    @property
    def lte(self):
        """ 将`lte`属性变更为动态属性
        """
        return self._lte

    @lte.setter
    def lte(self, value):
        """ Add input value type check

        :param value: User input lte value
        """
        # Ignore None
        if value is None:
            self._lte = value
            return

        # check input value type
        if not isinstance(value, int) and not isinstance(value, float):
            raise TypeError("property `lte` must be type of int or float")

        self._lte = value
