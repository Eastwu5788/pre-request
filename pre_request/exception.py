# !/usr/local/python/bin/python
# -*- coding: utf-8 -*-
# (C) Wu Dong, 2019
# All rights reserved
# @Author: 'Wu Dong <wudong@eastwu.cn>'
# @Time: '2020-03-17 15:39'


class PreRequestException(Exception):
    """ Pre-request 异常基类
    """


class ParamsValueError(ValueError):
    """自定义异常"""

    def __init__(self, code, **context):
        super().__init__()
        self.code = code
        self.context = context

    def form_message(self):  # noqa: disable
        """
        格式化JSON格式的错误消息
        :return:
        """
        message = "参数检测失败，请检查您的输入!"
        param_filter = self.context["filter"]

        if self.code == 560:
            message = "%s字段不能为空!" % param_filter.key

        elif self.code == 561:
            message = "%s字段长度不在限定范围内!" % param_filter.key

        elif self.code == 562:
            message = "%s字段无法转换成(%s)类型!" % (param_filter.key, param_filter.rule.direct_type.__name__)

        elif self.code == 563:
            message = "%s字段的取值只能是以下几种%s!" % (param_filter.key, str(param_filter.rule.enum))

        elif self.code == 564:
            message = "%s字段不符合邮件格式!" % param_filter.key

        elif self.code == 565:
            message = "%s字段不符合手机号格式!" % param_filter.key

        elif self.code == 566:
            message = "%s字段不符合格式要求!" % param_filter.key

        elif self.code == 567:
            message = "%s字段取值不在限定范围内!" % param_filter.key

        elif self.code == 568:
            message = "%s字段必须大于%s!" % (param_filter.key, str(param_filter.rule.gt))

        elif self.code == 570:
            message = "%s字段无法通过json进行解析" % param_filter.key

        elif self.code == 571:
            message = "%s字段必须大于等于%s!" % (param_filter.key, str(param_filter.rule.gte))

        elif self.code == 572:
            message = "%s字段必须小于%s!" % (param_filter.key, str(param_filter.rule.lt))

        elif self.code == 573:
            message = "%s字段必须小于等于%s!" % (param_filter.key, str(param_filter.rule.lte))

        elif self.code == 574:
            message = "%s字段长度必须大于%s!" % (param_filter.key, str(param_filter.rule.gt))

        elif self.code == 575:
            message = "%s字段长度必须大于等于%s!" % (param_filter.key, str(param_filter.rule.gte))

        elif self.code == 576:
            message = "%s字段长度必须小于%s!" % (param_filter.key, str(param_filter.rule.lt))

        elif self.code == 577:
            message = "%s字段长度必须小于等于%s!" % (param_filter.key, str(param_filter.rule.lte))

        elif self.code == 578:
            message = "%s字段必须等于%s!" % (param_filter.key, str(param_filter.rule.eq))

        elif self.code == 579:
            message = "%s字段不能等于%s!" % (param_filter.key, str(param_filter.rule.neq))

        return message
