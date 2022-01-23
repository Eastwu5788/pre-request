Validate Rules
=====================

**Control:**

==============   ==============================================
  Rule                      Desc
==============   ==============================================
  type              Direct type
  required          Param is required
  default          Default value if param is empty
  dest             Direct key for result
required_with      Required with other key
 location           Which location to read value for request
 skip               Skip all of the filters
==============   ==============================================

**Other:**

==============   ==============================================
  Rule                      Desc
==============   ==============================================
  json              Json deserialize value
  callback          Custom callback function
==============   ==============================================

**Fields:**

===========   ==============================================
  Rule                      Desc
===========   ==============================================
  eq_key          Field equal to another field
  neq_key        Field not equal to another field
  gt_key        Field greater than another field
  gte_key       Field greater than or equal to another field
  lt_key        Field less than another field
  lte_key       Field less than or equal to another field
===========   ==============================================

**Network:**

===========   ==========================================
  Rule                      Desc
===========   ==========================================
  ipv4           Internet protocol address IPv4
  ipv6           Internet protocol address IPv6
  mac           Media access control address MAC
===========   ==========================================

**Strings:**

===============   ==========================================
  Rule                      Desc
===============   ==========================================
  len               Content length for string or array
  trim              Trim space characters
  reg               Regex expression
 contains           Contains
 contains_any       Contains any items
 excludes           Excludes
 startswith         Starts with
 endswith           Ends with
 lower              Lowercase
 upper              Uppercase
 Split              Split string with special character
===============   ==========================================

**Format:**

===============   ==========================================
  Rule                      Desc
===============   ==========================================
    fmt              `date` or `datetime` format
  latitude            Latitude
  longitude           Longitude
  structure        Describe substructure for array or dict
   multi           Value is array
   deep               Find value from substructure
   enum             Enum value
===============   ==========================================

**Comparison:**

===============   ==========================================
  Rule                      Desc
===============   ==========================================
   eq                   Equals
   neq                  Not equal
   gt                   Greater than
   gte                  Greater than or equal
   lt                   Less than
   lte                  Less than or equal
===============   ==========================================


location
-------------

By default, `pre-request` try to parse values form `flask.Request.values` and `flask.Request.json`. Use `location`
to specify location to get values. current support ["args", "form", "values", "headers", "cookies", "json"]

::

  params = {
    "Access-Token": Rule(location="headers"),
    "userId": Rule(location=["cookies", "headers", "args"])
  }


deep
---------

By default, `pre-request` can parse value from complex structure. we can use `deep=False` to turn off this feature, pre-request
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

`pre-request` try to convert value to special type.

::

 params = {
    "userId": Rule(type=int)
 }


skip
-------

`pre-request` will skip validate value at this field. we will put origin value in the result structure.

::

 params = {
    "userName": Rule(skip=True)
 }


multi
--------

if you set `multi=True`, we will check every items in array. otherwise it will be regarded as a whole。

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

`pre-request` validate the value is not None or user do not input this value. Specially, if user don't input this value and `skip=True`,
`pre-request` will fill it with `missing` type.

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

`pre-request` will fill the default value into the field only if the field is not required and current value is None

::

  params = {
    "nickName": Rule(required=False, default="张三")
  }


split
--------

`pre-request` will split origin string value with special char and the check rule will filter to every value in the result array。

::

  params = {
    "userId": Rule(int, split=",")
  }


trim
------

`pre-request` will try to remove the space characters at the beginning and end of the string.

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

`pre-request` will convert all characters in the string to lowercase style.

::

  params = {
    "nickName": Rule(lower=True)
  }


upper
------

`pre-request` will convert all characters in the string to uppercase style.

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

Provides the style when the string is converted to `datetime` or `date` type. This is valid only on `type=datetime.datetime`


::

  params = {
    "birthday": Rule(type=datetime.datetime, fmt="%Y-%m-%d"),
    "otherDate": Rule(type=datetime.date, fmt="%Y-%m-%d")
  }


latitude / longitude
--------------------

Ensure that the field entered by the user conform to the `latitude/longitude` format.

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
    "userId": Rule(type=int, dest="user_id")
  }


json
----------

We will try to use the `json.loads` method to parse the value of the parameter to convert it into
a `list` or `dict` type.


callback
---------------

If the filters we provide cannot meet your needs, you can pass in the parse function you defied
through the `callback` method.

::

  def hand(value):
    if value <= 10:
        raise ParamsValueError("'userId' must be greater than 10")
    return value + 100

  params = {
    "userId": Rule(type=int, callback=hand)
  }
