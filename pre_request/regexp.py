# -*- coding: utf-8 -*-
# sys
import re

# project
from .macro import (
    K_FILE_REG,
    K_LATITUDE_REG,
    K_LONGITUDE_REG,
    K_MAC_REG,
)


class Regexp:
    """ Base class of regexp handler
    """
    def __init__(self, regex, flags=0):
        if isinstance(regex, str):
            regex = re.compile(regex, flags)

        self.regex = regex

    def __call__(self, data):
        return self.regex.match(data or '')


class FileRegexp(Regexp):
    """ Regexp handler class for file
    """
    def __init__(self):
        super().__init__(K_FILE_REG, re.IGNORECASE)

    def __call__(self, f=None):
        return super().__call__(f)


class MacRegexp(Regexp):
    """ Regexp handler class for mac address
    """
    def __init__(self):
        super().__init__(K_MAC_REG, re.IGNORECASE)

    def __call__(self, mac=None):
        return super().__call__(mac)


class LatitudeRegexp(Regexp):
    """ Regexp handler class for latitude
    """

    def __init__(self):
        super().__init__(K_LATITUDE_REG, re.IGNORECASE)

    def __call__(self, address=None):
        return super().__call__(address)


class LongitudeRegexp(Regexp):
    """ Regexp handler class for longitude
    """
    def __init__(self):
        super().__init__(K_LONGITUDE_REG, re.IGNORECASE)

    def __call__(self, address=None):
        return super().__call__(address)
