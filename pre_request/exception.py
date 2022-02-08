# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2019
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-03-17 15:39'


class ParamsValueError(ValueError):
    """ Invalid input params value exception
    """

    def __init__(self, message: str):
        super().__init__()
        self.message = message

    def __str__(self):
        return self.message
