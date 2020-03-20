# pre-request
[![Build Status](https://www.travis-ci.org/Eastwu5788/pre-request.svg?branch=master)](https://www.travis-ci.org/Eastwu5788/pre-request) 
[![Coverage Status](https://coveralls.io/repos/github/Eastwu5788/pre-request/badge.svg?branch=master)](https://coveralls.io/github/Eastwu5788/pre-request?branch=master) 
[![PyPI - License](https://img.shields.io/pypi/l/pre-request?color=brightgreen)](https://github.com/Eastwu5788/pre-request/blob/develop/LICENSE) 
[![Documentation Status](https://readthedocs.org/projects/pre-request/badge/?version=latest)](https://pre-request.readthedocs.io/en/latest/?badge=latest) 
[![PyPI](https://img.shields.io/pypi/v/pre-request)](https://pypi.org/project/pre-request/)


欢迎您使用pre-request框架，pre-request致力于简化请求参数验证工作。为Flask的
网络请求参数验证提供了解决方案。

pre-request提供了非常方便的使用的方法，也提供了灵活的扩展接口方便您实现自定义的
业务逻辑。


### 特点
1. 验证邮箱、手机号等特殊字段是否符合要求
2. 格式限制和转换处理，如果类型不符合或者无法转换成需求的类型，则抛出错误
3. 取值范围限制，显示参数的取值内容的范围
4. 请求参数为空和默认值处理，如果允许为空则可以设置默认值
5. 用户可以自定义callback, 自己处理任何参数（callback的调用在所有filter处理之后）
6. 可以将字段映射为内部使用的字段

### 安装
```
pip install pre-request
```

### 快速开始
1. 导入处理请求参数的装饰器
```
from pre_request import filter_params
```


2. 导入参数规则类
```
from pre_request import Rule, Length
```


3. 设置请求参数规则
```
field = {
    "age": Rule(direct_type=int, enum=[1, 2]),
    "name": Rule(length=Length(6, 12)),
    "email": Rule(email=True),
    "mobile": Rule(mobile=True),
    "empty": Rule(allow_empty=True, default="sssss_empty"),
    "range": Rule(direct_type=int, range=Range(10, 30)),
    "reg": Rule(reg=r'^h\w{3,5}o$', key_map="reg_exp"),
    "trim": Rule(trim=True, json=True),
    "call": Rule(direct_type=int, callback=lambda x: x+100)
}
```


4. 通过@filter_params()装饰器，过滤请求参数.注意在正常处理函数中添加params参数，接收过滤后的请求参数
```
# 不指定get和post时，不论get请求或者post请求都会使用同一个过滤参数
# 如果指定了get或者post时，直接设置的过滤参数会被覆盖
@app.route("/test", methods=['get', 'post'])
@filter_params(field)
def test_handler(params=None):
    return str(params)
```


5. 单独设置某一个请求的get或post请求
```
# 单独设置get请求的过滤参数
@app.route("/get", methods=['get'])
@filter_params(get=get_field)
def get_handler(params=None):
    return str(params)
    
# 单独设置post请求的过滤参数
@app.route("/post", methods=['post'])
@filter_params(post=post_field)
def post_handler(params=None):
    return str(params)
```


6. 也可以同时设置get和post请求的不同过滤参数
```
# 同时设置get和post的过滤参数
@app.route("/all", methods=['get', 'post'])
@filter_params(get=get_field, post=post_field)
def all_handler(params=None):
    return str(params)
```


7. 指定响应类型，通过response参数指定响应类型为json或者html
```
# 方法视图
@filter_params(get=get_field, response='json')
def get(self, params=None):
return str(params)

@filter_params(post=post_field, response='html')
def post(self, params=None):
return str(params)
```

### Rule规则参数介绍
```
# 字段目标数据类型
self.direct_type = kwargs.get("direct_type", str)

# 当前字段是否允许为空
self.allow_empty = kwargs.get("allow_empty", False)
# 当前字段默认值，如果不允许为空，则次字段无意义
self.default = kwargs.get("default", None)
# 去除前后的空格
self.trim = kwargs.get("trim", False)

# 字段枚举值设置
self.enum = kwargs.get("enum", list())
# range,整数范围限定, 只在direct_type为数字时有效
self.range = kwargs.get("range", Range())

# 正则表达式
self.reg = kwargs.get("reg", None)
# Email判断
self.email = kwargs.get("email", False)
# 手机号判断
self.mobile = kwargs.get("mobile", False)

# 字符串长度判断
self.len = kwargs.get("length", Length())

# key映射
self.key_map = kwargs.get("key_map", None)

# 是否需要进行json解析
self.json_load = kwargs.get("json", False)

# 自定义处理callback, 在所有的filter处理完成后，通过callback回调给用户进行自定义处理
self.callback = kwargs.get("callback", None)
```
