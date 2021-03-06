Validate Rules
=====================

location
-------------

By default, pre-request try to parse values form `flask.Request.values` and `flask.Request.json`. Use `location`
to specify location to pull the values from. current support ["args", "form", "values", "headers", "cookies", "json"]

::

  params = {
    "Access-Token": Rule(location="headers"),
    "userId": Rule(location=["cookies", "headers", "args"])
  }


deep
---------

By default, pre-request can parse value from complex structure. we can use `deep=False` to turn off this feature, pre-request
will parse values from top level.

::

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

Pre-request try to convert value type to special type.

::

 params = {
    "userId": Rule(type=int)
 }


skip
-------

Tells the pre-request to skip validate this field. we will put origin value in the result structure.

::

 params = {
    "userName": Rule(skip=True)
 }


multi
--------

Pre-request try to convert input value to list type. if you set multi value to false and input value is the type of list,
pre-request will use last value as input value. You can use `split` or `json` to get list type of input.

::

 params = {
    "userIds": Rule(type=int, multi=True)
 }


structure
-------------
You can use `structure` field to define sub structure in array. This field will be only valid in `multi=True`.

::

params = {
    "friends": Rule(multi=True, structure={
        "userId": Rule(type=int, required=True),
        "userName": Rule(type=str, required=True)
    })
}


required
----------

Pre-request validate the value is not None or user do not input this value.


::

 params = {
    "profile": Rule(required=False)
 }


required_with
---------------

The field under validation must be present and not empty only if any of the other specified fields are present.

::

 params = {
     "nickName": Rule(required=False),
     "profile": Rule(required=False, required_with="nickName")
 }


default
---------

Pre-request will fill the default value into the field only if the field is not required and current value is None

::

  params = {
    "nickName": Rule(required=False, default="张三")
  }


split
--------

Pre-request will split origin string value with special char and the check rule will filter to every value in the result array。

::

  params = {
    "userId": Rule(int, split=",")
  }


trim
------

Pre-request will try to remove the space characters at the beginning and end of the string.

::

 params = {
    "nickName": Rule(trim=True)
 }


enum
--------

Ensure that the parameters entered by the user are within the specified specific value range.

::

 params = {
    "gender": Rule(direct_type=int, enum=[1, 2])
 }


reg
-------

Use regular expressions to verity that the user input string meets the requirements.

::

 params = {
    "tradeDate": Rule(reg=r"^[1-9]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1])$")
 }


email
-------

Ensure that the field entered by the user conform to the email address format.

::

  params = {
    "email": Rule(email=True)
  }


mobile
---------

Ensure that the field entered by the user conform to the mobile phone number format.

::

  params = {
    "mobile": Rule(mobile=True)
  }


contains
----------

Ensure that the field entered by the user contain all of the special value.

::

  params = {
    "content": Rule(contains=["你好", "再见"])
  }


contains_any
--------------

Ensure that the field entered by the user contain any of the special value.

::

  params = {
    "content": Rule(contains_any=["你好", "再见"])
  }

excludes
-----------

Ensure that the field entered by the user can not contain any of special value.

::

 params = {
    "content": Rule(excludes=["张三", "李四"])
 }


startswith
------------

Ensure that the input string value must be start with special substring

::

 params = {
    "nickName": Rule(startswith="CN")
 }


endswith
----------

Ensure that the input string value must be end with special substring

::

 params = {
    "email": Rule(endswith="@eastwu.cn")
 }


lower
--------

Pre-request will convert all characters in the string to lowercase style.

::

  params = {
    "nickName": Rule(lower=True)
  }


upper
------

Pre-request will convert all characters in the string to uppercase style.

::

  params = {
    "country": Rule(upper=True)
  }


ipv4/ipv6
------------

Ensure that the field entered by the user conform to the ipv4/6 format.

::

  params = {
    "ip4": Rule(ipv4=True)
    "ip6": Rule(ipv6=True)
  }


mac
-------

Ensure that the field entered by the user conform to the MAC address format.

::

  params = {
    "macAddress": Rule(mac=True)
  }


fmt
--------

Provides the style when the string is converted to `datetime` type. This is valid only on `type=datetime.datetime`


::

  params = {
    "birthday": Rule(type=datetime.datetime, fmt="%Y-%m-%d")
  }


latitude / longitude
--------------------

Ensure that the field entered by the user conform to the latitude/longitude format.

::

  params = {
    "latitude": Rule(latitude=True),
    "longitude": Rule(longitude=True)
  }


eq / eq_key
-----------

Used to check whether the user input parameter is equal  to another value or another parameter.

::

  params = {
    "userId": Rule(eq=10086),
    "userId2": Rule(eq_key="userId")
  }


neq / neq_key
----------------

Used to check whether the user input parameter is not equal  to another value or another parameter.

::

 params = {
    "userId": Rule(neq=0),
    "forbidUserId": Rule(neq_key="userId")
 }


gt / gt_key
---------------

Used to check whether the user input parameter is great than another value or another parameter.

::

  params = {
      "kidAge": Rule(type=int, gt=0),
      "fatherAge": Rule(type=int, gt_key="kidAge")
  }


gte / gte_key
-----------------

Used to check whether the user input parameter is great than or equal to another value or another parameter.


::

  params = {
      "kidAge": Rule(type=int, gte=0),
      "brotherAge": Rule(type=int, gte_key="kidAge")
  }



lt / lt_key
-----------------

Used to check whether the user input parameter is less than another value or another parameter.

::

  params = {
      "fatherAge": Rule(type=int, lt=100),
      "kidAge": Rule(type=int, lt_key="fatherAge")
  }


lte / lte_key
-----------------

Used to check whether the user input parameter is less than or equal to another value or another parameter.

::

  params = {
      "fatherAge": Rule(type=int, lte=100),
      "kidAge": Rule(type=int, lte_key="fatherAge")
  }



dest
------------

We will convert the key of the parameter to another value specified.

::

  params = {
    "userId": Rule(direct_type=int, dest="user_id")
  }


json
----------

We will try to use the `json.loads` method to parse the value of the parameter to convert it into
a `list` or `dict` type.


call_back
---------------

If the function we provide cannot meet your needs, you can pass in the parse function you defied
through the `call_back` method.

::

  def hand(value):
    return value + 100

  params = {
    "userId": Rule(direct_type=int, call_back=hand)
  }
