# -*- coding: utf-8 -*-
# sys
import re


# email regexp
K_EMAIL_REG = r'^[A-Za-z\d]+([-_.][A-Za-z\d]+)*@([A-Za-z\d]+[-.])+[A-Za-z\d]{2,4}$'


# mobile regexp
K_MOBILE_REG = r'^0\d{2,3}\d{7,8}$|^1[3578]\d{9}$|^14[579]\d{8}$'


# file path regexp
K_FILE_REG = r'^(?<1>.*[\\/])(?<2>.+)\.(?<3>.+)?$|^(?<1>.*[\\/])(?<2>.+)$|^(?<2>.+)\.(?<3>.+)?$|^(?<2>.+)$'


# mac address regexp
K_MAC_REG = r'^([0-9a-fA-F][0-9a-fA-F]:){5}([0-9a-fA-F][0-9a-fA-F])$'


# latitude regexp
K_LATITUDE_REG = r'^[\-\+]?((0|([1-8]\d?))(\.\d{1,10})?|90(\.0{1,10})?)$'
# longitude regexp
K_LONGITUDE_REG = r'^[\-\+]?(0(\.\d{1,10})?|([1-9](\d)?)(\.\d{1,10})?|1[0-7]\d{1}(\.\d{1,10})?|180\.0{1,10})$'


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


class FileRegexp(Regexp):
    """ Regexp handler class for file
    """
    def __init__(self):
        super(FileRegexp, self).__init__(K_FILE_REG, re.IGNORECASE)

    def __call__(self, f=None):
        return super(FileRegexp, self).__call__(f)


class MacRegexp(Regexp):
    """ Regexp handler class for mac address
    """
    def __init__(self):
        super(MacRegexp, self).__init__(K_MAC_REG, re.IGNORECASE)

    def __call__(self, mac=None):
        return super(MacRegexp, self).__call__(mac)


class LatitudeRegexp(Regexp):
    """ Regexp handler class for latitude
    """

    def __init__(self):
        super(LatitudeRegexp, self).__init__(K_LATITUDE_REG, re.IGNORECASE)

    def __call__(self, address=None):
        return super(LatitudeRegexp, self).__call__(address)


class LongitudeRegexp(Regexp):
    """ Regexp handler class for longitude
    """
    def __init__(self):
        super(LongitudeRegexp, self).__init__(K_LONGITUDE_REG, re.IGNORECASE)

    def __call__(self, address=None):
        return super(LongitudeRegexp, self).__call__(address)
