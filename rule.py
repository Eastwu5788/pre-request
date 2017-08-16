from flask import request, make_response
import json
import MySQLdb
import re
from functools import wraps

_false_str_list = ["False", "false", "No", "no", "0", "None", "", "[]", "()", "{}", "0.0"]


class ParamsValueError(ValueError):
    """自定义异常"""
    def __init__(self, code, value):
        self.code = code
        self.value = value


class Length(object):

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


class BaseResponse(object):
    def __init__(self, message=None, code=500):
        self.message = message
        self.code = code

    def __call__(self, message=None, code=None):
        if not message:
            message = self.message
        if not code:
            code = self.code

        return {"code": code, "message": message}


class JSONResponse(BaseResponse):
    def __call__(self, message=None, code=500):
        result = super(JSONResponse, self).__call__(message, code)
        response = make_response(json.dumps(result))
        response.headers["Content-Type"] = "application/json; charset=utf-8"
        return response


class HTMLResponse(BaseResponse):
    def __call__(self, message=None, code=500):
        result = super(HTMLResponse, self).__call__(message, code)
        html = '<p>code:%s message:%s</p>' % (result["code"], result["message"])
        response = make_response(html)
        response.headers["Content-Type"] = "text/html; charset=utf-8"
        return response


RESPONSE = JSONResponse("请求参数错误!", 500)


def filter_params(rules=None, **options):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 过滤规则判断
            if not options and not rules:
                return func(*args, **kwargs)

            # 如果设置了get或者post方法的过滤方式，则优先处理
            if request.method == "GET":
                param_rules = options.get("get")
            else:
                param_rules = options.get("post")

            # 如果未处理get或者post，则使用rules
            if not param_rules:
                if rules:
                    param_rules = rules
                else:
                    return func(*args, **kwargs)

            result = dict()
            for key, value in param_rules.items():
                try:
                    result[key] = get_param(key, value)
                except ParamsValueError as error:
                    return get_response_with_error(error, options.get("response"))

            kwargs = dict({"params": result}, **kwargs)

            return func(*args, **kwargs,)
        return wrapper
    return decorator


def get_response_with_error(error=None, response=None):
    """
    获取出错时的响应模式
    :param error: 自定义错误
    :param response: 用户定义响应样式
    """
    # 使用特定的响应模式
    if response == 'json':
        return JSONResponse(error.value, error.code)()
    elif response == 'html':
        return HTMLResponse(error.value, error.code)()
    # 未预料的情况，则使用RESPONSE中定义的响应模式
    else:
        return RESPONSE(error.value, error.code)


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
        raise ParamsValueError(500, error_str)

    # 默认值处理
    if rule.allow_empty and not param:
        param = rule.default

    # 字段长度校验
    if rule.len and rule.len.need_check():
        if not rule.len.check_length(param):
            raise ParamsValueError(500, "%s字段的长度超出限定范围" % param_key)

    # 类型处理
    param = trans_type_param(param, rule)

    # 枚举判断
    if rule.enum and param not in rule.enum:
        err_str = '"%s"字段超出取值范围:%s' % (param_key, str(rule.enum))
        raise ParamsValueError(500, err_str)

    # 邮箱判断
    if rule.email:
        message = '%s字段不符合Email格式' % param_key
        EmailRegexp(message)(param)

    # 手机号判断
    if rule.mobile:
        message = '%s字段不符合手机号格式' % param_key
        MobileRegexp(message)(param)

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
            raise ParamsValueError(500, "%s参数必须是%s类型" % (param, rule.direct_type.__name__))


class Regexp(object):
    def __init__(self, regex, flags=0, message=None):
        if isinstance(regex, str):
            regex = re.compile(regex, flags)

        self.regex = regex
        self.message = message

    def __call__(self, data):
        match = self.regex.match(data or '')
        if not match:
            raise ParamsValueError(500, self.message)
        return True


class EmailRegexp(Regexp):

    def __init__(self, message=None):
        super(EmailRegexp, self).__init__(r'^.+@([^.@][^@]+)$', re.IGNORECASE, message)

    def __call__(self, email=None):
        return super(EmailRegexp, self).__call__(email)


class MobileRegexp(Regexp):

    def __init__(self, message=None):
        super(MobileRegexp, self).__init__(r'^0\d{2,3}\d{7,8}$|^1[358]\d{9}$|^147\d{8}', re.IGNORECASE, message)

    def __call__(self, mobile=None):
        return super(MobileRegexp, self).__call__(mobile)
