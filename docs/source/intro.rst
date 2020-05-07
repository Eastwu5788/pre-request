pre-request 规则介绍
=====================

欢迎您使用pre-request框架，pre-request致力于简化请求参数验证工作。为Flask的
网络请求参数验证提供了解决方案。

pre-request提供了非常方便的使用的方法，也提供了灵活的扩展接口方便您实现自定义的
业务逻辑。

下面我们将挨个介绍pre-request支持的所有规则


location
-------------

`location` 当请求体，请求头或者其它位置有相同的参数时，您可以使用 `location` 限制位置进行读取。
目前支持的位置包括 ["args", "form", "values", "headers", "cookies", "json"]

::

  # 限定参数从指定位置读取
  params = {
    "Access-Token": Rule(location="headers"),
    "userId": Rule(location=["cookies", "headers", "args"])
  }


deep
---------

`deep` 默认情况下，当前您的rule规则有层级关系时，pre-request会遵从您的层级关系从json中提取相同位置的参数进行填充。如果您指定了 `deep=False`
那么pre-request会放弃层级关系，直接从顶层参数中进行读取。

如果您不在json中传参数时，您可以使用 `.` 来标识层级关系。例如: `userInfo.socialInfo.age=13`

::

  # 限定参数的层级关系
  params = {
    "userInfo": {
        "userId": Rule(type=int, required=False),
        "socialInfo": {
            "gender": Rule(type=int, enum=[1, 2], default=1),
            "age": Rule(type=int, gte=18, lt=80),
            "country": Rule(required=True, deep=False)
        }
    }
  }

type
-------------

`type` 限制用户入参的数据类型。我们会尝试将用户入参中的参数类型转换成目标类型，如果尝试转换失败，
我们会输出特定错误码. 默认值 `str`

::

 # 限定用户的userId参数必须为int类型
 params = {
    "userId": Rule(type=int)
 }


skip
-------

`skip` 将标记参数为需要跳过，我们只是简单的将参数放置到结果集中，不会对其进行任何处理。默认值 `False`

::

 # 设定参数跳过所有检查
 params = {
    "userName": Rule(skip=True)
 }


required
----------

`required` 标记参数是否为用户必填项，如果是必填但是用户未传入或者传入空值，将会输出特定错误码。默认值 `True`

::

 # 设置某个参数为非必填
 params = {
    "profile": Rule(required=False)
 }


required_with
---------------

`required_with` 实现了参数联动必填确认，可以指定其他参数名称，当前其它参数填写时，当前参数也必须填写。默认值 `None`

::

 # 设置当用户昵称填写时，简介也必须填写
 params = {
     "nickName": Rule(required=False),
     "profile": Rule(required=False, required_with="nickName")
 }


default
---------

`default` 实现默认值填充，当参数不要求为必填时，如果用户未传参，可以使用 `default` 指定一个默认值。
注意: `default` 仅在 `required=False` 时有效。

::

  # 设置默认值
  params = {
    "nickName": Rule(required=False, default="张三")
  }


split
--------

`split` 实现将入参字符串按照指定字符串进行分割。默认值 `None`

::

  # 按','分割字符串
  params = {
    "userId": Rule(int, split=",")
  }


trim
------

`trim` 实现了字符串去除首尾空字符功能。默认值 `False`。

::

 # 设置自动去除字符串首尾空格
 params = {
    "nickName": Rule(trim=True)
 }


enum
--------

`enum` 验证参数枚举功能，确保用户入参仅能在可选范围内。默认值 `[]`

::

 # 设定用户性别为1或者2
 params = {
    "gender": Rule(direct_type=int, enum=[1, 2])
 }


reg
-------

`reg` 限定用户输入参数需要符合特定正则表达式。默认值 `None`

::

 # 设置日期必须符合日期正则
 params = {
    "tradeDate": Rule(reg=r"^[1-9]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1])$")
 }


email
-------

`email` 限制用户输入的参数必须符合邮箱格式，我们默认使用的邮箱正则表达式为 `^[A-Za-z\d]+([-_.][A-Za-z\d]+)*@([A-Za-z\d]+[-.])+[A-Za-z\d]{2,4}$`
如果您我们提供的正则表达式不符合您的要求，您可以使用 `reg` 参数进行自定义。默认值 `False`

::

  # 要求用户输入合法的email地址
  params = {
    "email": Rule(email=True)
  }


mobile
---------

`mobile` 限制用户输入的参数必须是合法的手机号，默认值 `False`

::

  # 要求用户输入合法的mobile号码
  params = {
    "mobile": Rule(mobile=True)
  }


contains
----------

`contains` 限定用户输入的字符串必须包含所有指定的子字符串，默认值 `[]`

::

  # 要求用户输入的内容必须包含 "你好" 和 "再见" 两个字符串
  params = {
    "content": Rule(contains=["你好", "再见"])
  }


contains_any
--------------

`contains_any` 要求用户输入的字符串包含任意一个子字符串，默认值 `[]`

::

  # 要求用户输入的内容必须包含 "你好" 或者 "再见" 两个子字符串中的一个
  params = {
    "content": Rule(contains_any=["你好", "再见"])
  }

excludes
-----------

`excludes` 用于限制用户输入的内容禁止包含特定的子字符串。默认值 `[]`

::

 # 要求用户输入的内容禁止包含"张三","李四"两个子字符串
 params = {
    "content": Rule(excludes=["张三", "李四"])
 }


startswith
------------

`startswith` 要求用户输入的字符串必须以特定子字符串开头。默认值 `None`

::

 # 要求用户昵称必须以 "CN" 开头
 params = {
    "nickName": Rule(startswith="CN")
 }


endswith
----------

`endswith` 要求用户输入的字符串必须以特定子字符串结尾。默认值 `None`

::

 # 要求用户邮箱必须以 "@eastwu.cn" 结尾
 params = {
    "email": Rule(endswith="@eastwu.cn")
 }


lower
--------

`lower` 会尝试将用户输入的字符串转换成小写。默认值 `False`

::

  # 尝试将用户输入转换成小写
  params = {
    "nickName": Rule(lower=True)
  }


upper
------

`upper` 会尝试将用户输入的字符串转换成大写。默认值 `False`

::

  # 尝试将用户输入转换成大写
  params = {
    "country": Rule(upper=True)
  }


ipv4/ipv6
------------

`ipv4` 检查用户输入的内容是否是合法的IPV4地址。默认值 `False`。

`ipv6` 检查用户输入的内容是否是合法的ipv6地址。默认值 `False`。

::

  params = {
    "ip4": Rule(ipv4=True)
    "ip6": Rule(ipv6=True)
  }


mac
-------

`mac` 检查用户输入内容是否是合法的网卡 MAC 地址。默认值 `False`

::

  params = {
    "macAddress": Rule(mac=True)
  }


fmt
--------

将字符串转换成`datetime`类型时的格式化样例. 注意`fmt`参数仅在`type=datetime.datetime`时有效

::

  params = {
    "birthday": Rule(type=datetime.datetime, fmt="%Y-%m-%d")
  }


latitude / longitude
--------------------

检查用户输入的参数是否是合法的经纬度数据。默认值 `False`

::

  params = {
    "latitude": Rule(latitude=True),
    "longitude": Rule(longitude=True)
  }


eq / eq_key
-----------

`eq` 用于检查用户输入的内容必须与特定值相等。默认值 `None`。

`eq_key` 用于限定用户输入内容必须与另外一个参数值相等。默认值 `None`。

::

  params = {
    "userId": Rule(eq=10086),
    "userId2": Rule(eq_key="userId")
  }


neq / neq_key
----------------

`neq` 用于检查用户输入的内容不能与特定值相等。默认值 `None`。

`neq_key` 用于限定用户输入内容不能与另一个参数值相等。默认值 `None`。

::

 params = {
    "userId": Rule(neq=0),
    "forbidUserId": Rule(neq_key="userId")
 }


gt / gt_key
---------------

`gt` 用于检查用户输入内容必须大于特定值，如果字段类型为int，则判断大小，如果为 str 则判断字符串长度大小。默认值为 `None`。

`gt_key` 用于判断参数的值必须大于另一个参数。默认值 `None`。


gte / gte_key
-----------------

使用方法同 gt / gt_key，表示大于等于的判断

lt / lt_key
-----------------

使用方法同 gt / gt_key, 表示小于的判断

lte / lte_key
-----------------

使用方法同 gt / gt_key 表示小于等于的判断


key_map
------------

`kay_map` 用于将用户传入的参数名称映射为特定的字符串。默认值为 `None`

::

  params = {
    "userId": Rule(direct_type=int, key_map="user_id")
  }


json
----------

`json` 如果用户的参数内容是json字符串，可以使用此参数尝试将其解析成对象。默认值 `False`


call_back
---------------

`call_back` 用户自定义处理参数内容，当我们提供的处理器无法满足您的需求时，可以尝试自己实现处理器

::

  def hand(value):
    return value + 100

  params = {
    "userId": Rule(direct_type=int, call_back=hand)
  }
