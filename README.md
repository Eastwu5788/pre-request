# pre-request

# 介绍
针对Flask、Tornado框架设计的请求预处理类

# 用法
1. 将pre-request包导入到项目中


2. 导入处理请求参数的装饰器
```
# 在Flask环境下
from pre_request.flask import filter_params

# 在Tornado环境下
from pre_request.tornado import filter_params
```


3. 导入参数规则类(Flask、Tornado通用)
```
from pre_request.filter_rules import Rule, Length
```


４. 设置请求参数规则
```
field = {
    "age": Rule(direct_type=int, enum=[1, 2]),
    "name": Rule(length=Length(6, 12)),
    "email": Rule(email=True),
    "mobile": Rule(mobile=True),
    "empty": Rule(allow_empty=True, default="sssss_empty")
}
```


５. 通过@filter_params()装饰器，过滤请求参数.注意在正常处理函数中添加params参数，接收过滤后的请求参数
```
# 不指定get和post时，不论get请求或者post请求都会使用同一个过滤参数
# 如果指定了get或者post时，直接设置的过滤参数会被覆盖
@app.route("/test", methods=['get', 'post'])
@filter_params(field)
def test_handler(params=None):
    return str(params)
```


６. 单独设置某一个请求的get或post请求
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


７. 也可以同时设置get和post请求的不同过滤参数
```
# 同时设置get和post的过滤参数
@app.route("/all", methods=['get', 'post'])
@filter_params(get=get_field, post=post_field)
def all_handler(params=None):
    return str(params)
```


８. 指定响应类型，通过response参数指定响应类型为json或者html
```
# 方法视图
@filter_params(get=get_field, response='json')
def get(self, params=None):
return str(params)

@filter_params(post=post_field, response='html')
def post(self, params=None):
return str(params)
```


９. 修改默认响应类型,修改filter_response.py中的RESPONSE变量
```
RESPONSE = JSONResponse()
```


10. 设置自定义响应,主要是继承BaseResponse，具体实现可以参考JSONResponse或HTMLResponse类的实现
```
class JSONResponse(BaseResponse):
    """
    以JSON格式响应出错的情况
    """
    def __call__(self, handler=None, error=None, request_type=None):
        """
        :type error: 错误
        :param request_type: 请求类型
        :return:
        """
        result = super(JSONResponse, self).__call__(handler, error, request_type)
        # Flask的处理
        if self.request_type == RequestTypeEnum.Flask:
            from flask import make_response
            response = make_response(json.dumps(result))
            response.headers["Content-Type"] = "application/json; charset=utf-8"
            return response
        # Tornado的处理　
        else:
            self.handler.set_header("Content-Type", "application/json; charset=utf-8")
            return self.handler.write(json.dumps(result))
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
