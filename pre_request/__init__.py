# -*- coding: utf-8 -*-
# Copyright (c) 2017, Wu Dong
# All rights reserved.
# flake8: noqa
"""
Pre-request Library
~~~~~~~~~~~~~~~~~~~

Pre-request is a library, which help us deal with request params before handler.

Usage:
    >>> from pre_request import pre, Rule
    >>> @pre.catch(rule={"userId": Rule(direct_type=int)})
    >>> def handler_info(params):
    >>>     print(params)


:copyright: (c) 2020 by Wu Dong
:license: Apache 2.0, see LICENSE for more details.
"""
from .request import PreRequest as _PreRequest
from .response import BaseResponse
from .filters.base import BaseFilter
from .rules import Rule
from .exception import ParamsValueError
from .__version__ import __version__


pre = _PreRequest()
