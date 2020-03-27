# -*- coding: utf-8 -*-
"""
默认响应类型
"""
RESPONSE_TYPE = "json"


class Enum(set):

    def __getattr__(self, item):
        if item in self:
            return item
        raise AttributeError


RequestTypeEnum = Enum(["Flask", "Tornado"])
