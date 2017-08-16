# pre-request-flask

# 介绍
针对Flask框架设计的请求预处理类

# 用法
1. 设置请求参数规则
```
field = {
    "age": Rule(direct_type=int, enum=[1, 2]),
    "name": Rule(length=Length(6, 12)),
    "email": Rule(email=True),
    "mobile": Rule(mobile=True),
    "empty": Rule(allow_empty=True, default="sssss_empty")
}
```
2. 通过@filter_params()装饰器，过滤请求参数.注意在正常处理函数中添加params参数，接收过滤后的请求参数
```
@app.route("/test", methods=['get', 'post'])
@filter_params(field)
def test_handler(params=None):
    return str(params)
```
# Rule规则参数介绍
```
# 当前字段是否允许为空
self.allow_empty = allow_empty
# 当前字段默认值，如果不允许为空，则次字段无意义
self.default = default
# 字段目标数据类型
self.direct_type = direct_type
# 字段枚举值，限定取值范围
self.enum = enum
# Email判断
self.email = email
# 手机号判断
self.mobile = mobile
# 字符串长度判断
self.len = length
# 字段是否是安全的，否则会进行转义，防止SQL注入
self.safe = safe
```
