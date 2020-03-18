# -*- coding: utf-8 -*-

import re
from .macro import K_EMAIL_REG, K_MOBILE_REG


class Regexp(object):
    """
    正则表达式基类
    """
    def __init__(self, regex, flags=0):
        if isinstance(regex, str):
            regex = re.compile(regex, flags)

        self.regex = regex

    def __call__(self, data):
        return self.regex.match(data or '')


class EmailRegexp(Regexp):
    """
    邮箱正则表达式
    """
    def __init__(self):
        # TODO：邮箱正则修改
        super(EmailRegexp, self).__init__(K_EMAIL_REG, re.IGNORECASE)

    def __call__(self, email=None):
        return super(EmailRegexp, self).__call__(email)


class MobileRegexp(Regexp):
    """
    手机号正则表达式
    """
    def __init__(self):
        super(MobileRegexp, self).__init__(K_MOBILE_REG, re.IGNORECASE)

    def __call__(self, mobile=None):
        return super(MobileRegexp, self).__call__(mobile)
