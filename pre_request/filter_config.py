from pre_request.filter_plugin import *
from enum import Enum


"""
下方数组中的过滤器会依次被执行
"""
FILTER_LIST = [
    EmptyFilter,    # 1.判断字段是否为空的过滤器
    LengthFilter,   # 2.字符长度过滤器
    TypeFilter,     # 3.类型转换过滤器
    EnumFilter,     # 4.枚举过滤器
    EmailFilter,    # 5.邮箱过滤器
    MobileFilter,   # 6.手机号过滤器
]


"""邮箱正则表达式"""
K_EMAIL_REG = r'^.+@([^.@][^@]+)$'

"""手机号正则表达式"""
K_MOBILE_REG = r'^0\d{2,3}\d{7,8}$|^1[358]\d{9}$|^147\d{8}'


class RequestTypeEnum(Enum):
    """
    当前请求类型的枚举
    """
    Flask = 1
    Tornado = 2
    Django = 3


