# -*- coding: utf-8 -*-
# flake8: noqa
# sys
import re

# RFC5322
EMAIL_REG = r"""([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|"([]!#-[^-~ \t]|(\\[\t -~]))+")@([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\[[\t -Z^-~]*])"""
LATITUDE_REG = r"^[-+]?([1-8]?\d(\.\d+)?|90(\.0+)?)$"
LONGITUDE_REG = r"^[-+]?(180(\.0+)?|((1[0-7]\d)|([1-9]?\d))(\.\d+)?)$"
MAC_REG = r"[0-9a-f]{2}([-:])[0-9a-f]{2}(\1[0-9a-f]{2}){4}$"


email_regex = re.compile(EMAIL_REG)
latitude_regex = re.compile(LATITUDE_REG)
longitude_regex = re.compile(LONGITUDE_REG)
mac_regex = re.compile(MAC_REG)
