from flask import request
import MySQLdb

_false_str_list = ["False", "false", "No", "no", "0", "None", "", "[]", "()", "{}", "0.0"]


class ParamsValueError(ValueError):
    """自定义异常"""
    def __init__(self, value):
        self.value = value


class Rule(object):
    """
    字段遵守的规则定义类
    """
    def __init__(self, allow_empty=False, direct_type=str, default=None, enum=list(), safe=False):
        # 当前字段是否允许为空
        self.allow_empty = allow_empty
        # 当前字段默认值，如果不允许为空，则次字段无意义
        self.default = default
        # 字段目标数据类型
        self.direct_type = direct_type
        # 字段枚举值，限定取值范围
        self.enum = enum
        # 字段是否是安全的，否则会进行转义，防止SQL注入
        self.safe = safe


def get_params(rules=None):
    """
    获取请求的所有属性值
    :param rules: 请求规则
    :return: 属性字典
    """
    # 请求为空判断
    if not rules:
        return dict()
    # 规则类型判断
    if not isinstance(rules, dict):
        return dict()

    # 依次处理每一个键值对
    result = dict()
    for key, value in rules.items():
        result[key] = get_param(key, value)

    return result


def get_param(param_key=None, rule=None):
    """
    获取单个属性的取值
    :param param_key: key
    :param rule: 取值规则
    :type rule: Rule
    """
    param = request.values.get(param_key, default=None)

    # 非空判断
    if not rule.allow_empty and not param:
        error_str = "%s字段不能为空." % param_key
        raise ParamsValueError(error_str)

    # 类型处理
    try:
        param = trans_type_param(param, rule)
    except ParamsValueError as error:
        raise error

    # 枚举判断
    if rule.enum and param not in rule.enum:
        err_str = '"%s"字段超出取值范围:%s' % (param_key, str(rule.enum))
        raise ParamsValueError(err_str)

    return param


def trans_type_param(param, rule):
    direct_type = rule.direct_type

    # 初始类型就是字符串，并且默认是安全的，则不需要处理
    if isinstance(param, direct_type) and rule.safe:
        return param

    if direct_type == str:
        if rule.safe:
            return param
        else:
            param = MySQLdb.escape_string(param)
            if isinstance(param, bytes):
                param = param.decode('utf-8')
            return param
    # 特殊的字符串转bool类型
    elif direct_type == bool and param in _false_str_list:
        return False
    else:
        try:
            return rule.direct_type(param)
        except ValueError:
            raise ParamsValueError("%s参数必须是%s类型" % (param, rule.direct_type.__name__))