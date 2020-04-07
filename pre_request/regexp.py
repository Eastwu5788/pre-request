# -*- coding: utf-8 -*-
# sys
import re


# 邮箱正则表达式
K_EMAIL_REG = r'^[A-Za-z\d]+([-_.][A-Za-z\d]+)*@([A-Za-z\d]+[-.])+[A-Za-z\d]{2,4}$'


# 手机号正则表达式
K_MOBILE_REG = r'^0\d{2,3}\d{7,8}$|^1[3578]\d{9}$|^14[579]\d{8}$'


class Regexp:
    """ Base class of regexp handler
    """
    def __init__(self, regex, flags=0):
        if isinstance(regex, str):
            regex = re.compile(regex, flags)

        self.regex = regex

    def __call__(self, data):
        return self.regex.match(data or '')


class EmailRegexp(Regexp):
    """ Regexp handler class for email
    """
    def __init__(self):
        super(EmailRegexp, self).__init__(K_EMAIL_REG, re.IGNORECASE)

    def __call__(self, email=None):
        return super(EmailRegexp, self).__call__(email)


class MobileRegexp(Regexp):
    """ Regexp handler class for mobile
    """
    def __init__(self):
        super(MobileRegexp, self).__init__(K_MOBILE_REG, re.IGNORECASE)

    def __call__(self, mobile=None):
        return super(MobileRegexp, self).__call__(mobile)
