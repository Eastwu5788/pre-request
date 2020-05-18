# -*- coding: utf-8 -*-
from datetime import datetime


class Rule:  # pylint: disable=too-many-instance-attributes
    """ This class is designed to describe special rule that params must follow
    """

    def __init__(self, **kwargs):
        # 参数来源位置
        self.location = kwargs.get("location", None)
        # 字段目标数据类型
        self.direct_type = kwargs.get("type", str)
        # 不进行过滤，仅把参数加到结果集中
        self.skip = kwargs.get("skip", False)
        # 请求参数深度跟随
        self.deep = kwargs.get("deep", True)
        # 指定参数是否有多个，如果传入的是list时，multi=False会读取最后一个
        self.multi = kwargs.get("multi", False)

        # 当前字段是否是必填项
        self.required = kwargs.get("required", True)
        self.required_with = kwargs.get("required_with", None)

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

        # 判断字符串中包含某个子串
        self.contains = kwargs.get("contains", list())
        # 判断字符串包含任意子串
        self.contains_any = kwargs.get("contains_any", list())
        # 判断字符串中禁止包括某个子串
        self.excludes = kwargs.get("excludes", list())
        # 判断字符串开头
        self.startswith = kwargs.get("startswith", None)
        # 判断字符串结尾
        self.endswith = kwargs.get("endswith", None)
        # 字符串小写
        self.lower = kwargs.get("lower", False)
        # 字符串大写
        self.upper = kwargs.get("upper", False)
        # 是否是文件路径
        # self.file = kwargs.get("file", False)
        # 字符串分割
        self.split = kwargs.get("split", None)

        # 判断入参是否为ipv4/ipv6
        self.ipv4 = kwargs.get("ipv4", False)
        self.ipv6 = kwargs.get("ipv6", False)
        self.mac = kwargs.get("mac", False)

        # 判断入参是否为地理坐标 经度/维度
        self.latitude = kwargs.get("latitude", False)
        self.longitude = kwargs.get("longitude", False)

        # 日期格式化字符串
        self.fmt = kwargs.get("fmt", "%Y-%m-%d %H:%M:%S")

        # 跨字段验证
        self.eq_key = kwargs.get("eq_key", None)
        self.neq_key = kwargs.get("neq_key", None)
        self.gt_key = kwargs.get("gt_key", None)
        self.gte_key = kwargs.get("gte_key", None)
        self.lt_key = kwargs.get("lt_key", None)
        self.lte_key = kwargs.get("lte_key", None)

        # 等于/不等于
        self.eq = kwargs.get("eq", None)
        self.neq = kwargs.get("neq", None)

        # 范围限定 direct_type 为数字时限定数字大小，为字符串时限定字符串长度
        self.gt = kwargs.get("gt", None)
        self.gte = kwargs.get("gte", None)
        self.lt = kwargs.get("lt", None)
        self.lte = kwargs.get("lte", None)

        # key映射
        self.key_map = kwargs.get("dest", None)

        # 是否需要进行json解析
        self.json_load = kwargs.get("json", False)

        # 自定义处理callback, 在所有的filter处理完成后，通过callback回调给用户进行自定义处理
        self.callback = kwargs.get("callback", None)

    @property
    def gt(self):
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
        if not isinstance(value, (int, float, datetime)):
            raise TypeError("property `gt` must be type of int datetime or float")

        self._gt = value

    @property
    def gte(self):
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
        if not isinstance(value, (int, float, datetime)):
            raise TypeError("property `gte` must be type of int datetime or float")

        self._gte = value

    @property
    def lt(self):
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
        if not isinstance(value, (int, float, datetime)):
            raise TypeError("property `lt` must be type of int datetime or float")

        self._lt = value

    @property
    def lte(self):
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
        if not isinstance(value, (int, float, datetime)):
            raise TypeError("property `lte` must be type of int or float")

        self._lte = value

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, value):
        """ Add type check for key location
        """
        df_location = ["args", "form", "values", "headers", "cookies", "json"]

        if value is None:
            self._location = value
            return

        if not isinstance(value, str) and not isinstance(value, list):
            raise TypeError("location must be type of list or str")

        if not value:
            raise ValueError("location value is empty")

        if isinstance(value, str):
            value = [value]

        for location in value:
            if location not in df_location:
                raise ValueError("params `location` must be in %s" % df_location)

        self._location = value
