# -*- coding: utf-8 -*-

from .filter_plugin import *


"""
下方数组中的过滤器会依次被执行
"""
FILTER_LIST = [
    EmptyFilter,    # 1.判断字段是否为空的过滤器
    TrimFilter,     # 2.去除字符串两侧的空格
    LengthFilter,   # 3.字符长度过滤器
    RegexpFilter,   # 4.正则表达式过滤器
    TypeFilter,     # 5.类型转换过滤器
    RangeFilter,    # 6.取值范围过滤器
    EnumFilter,     # 7.枚举过滤器
    EmailFilter,    # 8.邮箱过滤器
    MobileFilter,   # 9.手机号过滤器
]


"""邮箱正则表达式"""
K_EMAIL_REG = r'^[A-Za-z\d]+([-_.][A-Za-z\d]+)*@([A-Za-z\d]+[-.])+[A-Za-z\d]{2,4}$'

"""手机号正则表达式"""
K_MOBILE_REG = r'^0\d{2,3}\d{7,8}$|^1[3578]\d{9}$|^14[579]\d{8}$'


"""
默认响应类型
"""
RESPONSE_TYPE = "json"


class Enum(set):

    def __getattr__(self, item):
        if item in self:
            return item
        raise AttributeError

RequestTypeEnum = Enum(["Flask", "Tornado", "Django"])



