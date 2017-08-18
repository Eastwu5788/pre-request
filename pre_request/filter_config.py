from pre_request.filter_plugin import *
from enum import Enum


"""
下方数组中的过滤器会依次被执行
"""
FILTER_LIST = [
    EmptyFilter,    # 1.判断字段是否为空的过滤器
    LengthFilter,   # 2.字符长度过滤器
    RegexpFilter,   # 3.正则表达式过滤器
    TypeFilter,     # 4.类型转换过滤器
    RangeFilter,    # 5.取值范围过滤器
    EnumFilter,     # 6.枚举过滤器
    EmailFilter,    # 7.邮箱过滤器
    MobileFilter,   # 8.手机号过滤器
]


"""邮箱正则表达式"""
K_EMAIL_REG = r'^[A-Za-z\d]+([-_.][A-Za-z\d]+)*@([A-Za-z\d]+[-.])+[A-Za-z\d]{2,4}$'

"""手机号正则表达式"""
K_MOBILE_REG = r'^0\d{2,3}\d{7,8}$|^1[3578]\d{9}$|^14[579]\d{8}$'


class RequestTypeEnum(Enum):
    """
    当前请求类型的枚举
    """
    Flask = 1
    Tornado = 2
    Django = 3


