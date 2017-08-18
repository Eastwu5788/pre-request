# -*- coding: utf-8 -*-

import json
from pre_request.filter_config import RequestTypeEnum, RESPONSE_TYPE
from pre_request.filter_error import ParamsValueError


class BaseResponse(object):
    """
    错误响应基类
    """
    def __init__(self, handler=None, error=None, request_type=RequestTypeEnum.Flask):
        self.handler = handler
        self.error = error
        self.request_type = request_type

    def __call__(self, handler=None, error=None, request_type=None):
        """
        :param error: 错误
        :type error: ParamsValueError
        :param request_type: 请求类型
        """
        if handler:
            self.handler = handler
        if error:
            self.error = error
        if request_type:
            self.request_type = request_type

        return {"code": self.error.code, "message": self.error.form_message()}


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
        if self.request_type == RequestTypeEnum.Flask:
            from flask import make_response
            response = make_response(json.dumps(result))
            response.headers["Content-Type"] = "application/json; charset=utf-8"
            return response
        else:
            self.handler.set_header("Content-Type", "application/json; charset=utf-8")
            return self.handler.write(json.dumps(result))


class HTMLResponse(BaseResponse):
    """
    以HTML格式响应出错的情况
    """
    def __call__(self, handler=None, error=None, request_type=None):
        """
        :type error: 错误
        :param request_type: 请求类型
        :return:
        """
        result = super(HTMLResponse, self).__call__(handler, error, request_type)
        if self.request_type == RequestTypeEnum.Flask:
            from flask import make_response
            html = '<p>code:%s message:%s</p>' % (result["code"], result["message"])
            response = make_response(html)
            response.headers["Content-Type"] = "text/html; charset=utf-8"
            return response
        else:
            html = '<p>code:%s message:%s</p>' % (result["code"], result["message"])
            self.handler.set_header("Content-Type", "text/html; charset=utf-8")
            return self.handler.write(html)


def get_response_with_error(handler=None, error=None, response=None, request_type=RequestTypeEnum.Flask):
    """
    获取出错时的响应模式
    :param error: 自定义错误
    :param response: 用户定义响应样式
    :param handler: 原始请求
    :param request_type: 请求类型
    """
    # 如果未设置响应类型，则使用配置文件中的响应类型
    if not response:
        response = RESPONSE_TYPE

    # 使用特定的响应模式
    if response == 'json':
        return JSONResponse(handler, error, request_type)()
    elif response == 'html':
        return HTMLResponse(handler, error, request_type)()
    # 未预料的情况，使用JSON格式的响应类型
    else:
        return JSONResponse(handler, error, request_type)()
