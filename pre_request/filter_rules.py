"""
该文件主要定义所有的规则处理类
"""


class Length(object):
    """
    使用Length类限定字符串长度范围
    """

    def __init__(self, min_len=-1, max_len=-1):
        """
        初始化字符串长度
        :param min_len: 字符串最小值，如果为0表示不加限制
        :param max_len: 字符串长度最大值，如果为0表示不加限制
        """
        self.min_len = min_len
        self.max_len = max_len
        if self.min_len != -1 and self.max_len != -1 and self.max_len < self.min_len:
            raise ValueError("字符串长度设置失败,最大长度不能小于最小长度!")

    def need_check(self):
        """是否需要进行长度校验"""
        return self.min_len != -1 or self.max_len != -1

    def check_length(self, ori_str=""):
        """检查字符串长度"""
        length = len(ori_str)
        if self.min_len != -1:
            if length < self.min_len:
                return False
        if self.max_len != -1:
            if length > self.max_len:
                return False
        return True


class Rule(object):
    """
    字段遵守的规则定义类
    """
    # TODO: 1.使用继承来扩展其它规则
    # TODO：3.正则、Range()
    # TODO: 4.字符串转义修改
    # TODO: 5.支持自定义规则
    def __init__(self, allow_empty=False, direct_type=str, default=None, enum=list(), email=False, mobile=False,
                 length=Length(), safe=False):
        # 当前字段是否允许为空
        self.allow_empty = allow_empty
        # 当前字段默认值，如果不允许为空，则次字段无意义
        self.default = default
        # 字段目标数据类型
        self.direct_type = direct_type
        # 字段枚举值，限定取值范围
        self.enum = enum
        # Email判断
        self.email = email
        # 手机号判断
        self.mobile = mobile
        # 字符串长度判断
        self.len = length
        # 字段是否是安全的，否则会进行转义，防止SQL注入
        self.safe = safe
