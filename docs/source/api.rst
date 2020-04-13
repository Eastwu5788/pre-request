.. _api:

API 参考
===============

.. module:: pre_request

这部分文档涵盖了 pre-request 的部分接口。对于那些 pre-request 依赖外部库的部分，我们这里提供部分最重要的文档，并且提供其官方文档的链接


Rule 参数规则定义
===================

.. class:: pre_request.Rule

    Rule 对象用于定义用户输入的参数应该遵守的规则，过滤器中会按照Rule中定义的规则依次进行检查

    .. attribute:: direct_type

    定义参数的目标数据类型


Request 请求处理类
====================

.. module:: pre_request.request

.. autoclass:: PreRequest
    :members:
    :show-inheritance:
    :inherited-members:

Filter 模块
==============

Email 邮箱过滤器
------------------

.. module:: pre_request.filters.email_filter

.. autoclass:: EmailFilter
    :members:
    :show-inheritance:
    :inherited-members:

Empty 空值过滤器
------------------

.. module:: pre_request.filters.empty_filter

.. autoclass:: EmptyFilter
    :members:
    :show-inheritance:
    :inherited-members:

Enum 枚举过滤器
-----------------

.. module:: pre_request.filters.enum_filter

.. autoclass:: EnumFilter
    :members:
    :show-inheritance:
    :inherited-members:

Equal 等值过滤器
-----------------

.. module:: pre_request.filters.equal_filter

.. autoclass:: EqualFilter
    :members:
    :show-inheritance:
    :inherited-members:
