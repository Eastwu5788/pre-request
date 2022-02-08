# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2021
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2022/2/8 9:06 上午'
from pre_request import Rule, Length, validator


rule = {
    "k1": Rule(type=float, gte=3, lte=10, required=True),
    "k2": Rule(type=int, required=False),
    "k3": Rule(type=str, required=True, len=Length(gte=3))
}


@validator(rule=rule)
def check_func(k1, k2=3, **kwargs):
    print(k1, k2, kwargs)


if __name__ == "__main__":
    check_func(5, k2=9, k3=308)
