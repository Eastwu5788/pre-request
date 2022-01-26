# -*- coding: utf-8 -*-
# flake8: noqa
# sys
import re


ALPHA_REG = r"^[a-zA-Z]+$"
ALPHA_NUMERIC_REG = r"^[a-zA-Z0-9]+$"
# RFC5322
EMAIL_REG = r"""([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|"([]!#-[^-~ \t]|(\\[\t -~]))+")@([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\[[\t -Z^-~]*])"""
LATITUDE_REG = r"^[-+]?([1-8]?\d(\.\d+)?|90(\.0+)?)$"
LONGITUDE_REG = r"^[-+]?(180(\.0+)?|((1[0-7]\d)|([1-9]?\d))(\.\d+)?)$"
MAC_REG = r"[0-9a-f]{2}([-:])[0-9a-f]{2}(\1[0-9a-f]{2}){4}$"
# DATA_URI_REG = r"^data:((?:\w+\/(?:([^;]|;[^;]).)+)?)"
NUMERIC_REG = r"^[-+]?[0-9]+(?:\.[0-9]+)?$"
NUMBER_REG = r"^[0-9]+$"
# BASE64_REG = r"^([A-Za-z0-9+/]{4})*([A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=|[A-Za-z0-9+/]{4})$"


REGEX_PARAMS = {
    "alpha": {
        "regex": re.compile(ALPHA_REG),
        "message": "'%s' must consist of alpha"
    },
    "alphanum": {
        "regex": re.compile(ALPHA_NUMERIC_REG),
        "message": "'%s' must consist of alpha or numeric"
    },
    "number": {
        "regex": re.compile(NUMBER_REG),
        "message": "'%s' must consist of number"
    },
    "numeric": {
        "regex": re.compile(NUMERIC_REG),
        "message": "'%s' must consist of numeric"
    },
    "mac": {
        "regex": re.compile(MAC_REG),
        "message": "'%s' is not a valid MAC address"
    },
    "latitude": {
        "regex": re.compile(LATITUDE_REG),
        "message": "'%s' is not a valid latitude value"
    },
    "longitude": {
        "regex": re.compile(LONGITUDE_REG),
        "message": "'%s' is not a valid longitude value"
    },
    "email": {
        "regex": re.compile(EMAIL_REG),
        "message": "'%s' is not a valid email address"
    },
    # "data_uri": {
    #     "regex": re.compile(DATA_URI_REG),
    #     "message": "'%s' is not a valid data uri"
    # },
}
