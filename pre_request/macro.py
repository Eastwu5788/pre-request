# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2020
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-08-25 09:46'

# Project config key
K_CONTENT_TYPE = "PRE_CONTENT_TYPE"
K_FUZZY = "PRE_FUZZY"
K_STORE_KEY = "PRE_STORE_KEY"
K_SKIP_FILTER = "PRE_SKIP_FILTER"

# Regexp key
# file path regexp
K_FILE_REG = r'^(?<1>.*[\\/])(?<2>.+)\.(?<3>.+)?$|^(?<1>.*[\\/])(?<2>.+)$|^(?<2>.+)\.(?<3>.+)?$|^(?<2>.+)$'
# mac address regexp
K_MAC_REG = r'^([0-9a-fA-F][0-9a-fA-F]:){5}([0-9a-fA-F][0-9a-fA-F])$'
# latitude regexp
K_LATITUDE_REG = r'^[\-\+]?((0|([1-8]\d?))(\.\d{1,10})?|90(\.0{1,10})?)$'
# longitude regexp
K_LONGITUDE_REG = r'^[\-\+]?(0(\.\d{1,10})?|([1-9](\d)?)(\.\d{1,10})?|1[0-7]\d{1}(\.\d{1,10})?|180\.0{1,10})$'
