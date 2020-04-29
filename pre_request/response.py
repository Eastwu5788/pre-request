# -*- coding: utf-8 -*-
import json


class BaseResponse:
    """
    错误响应基类
    """

    def __call__(self, fuzzy=False, error=None):
        """
        :param error: 错误
        :type error: ParamsValueError
        """
        if error:
            self.error = error

        return {"respCode": self.error.code, "respMsg": self.error.form_message(fuzzy), "result": {}}


class JSONResponse(BaseResponse):
    """ 以JSON格式响应出错的情况
    """

    def __call__(self, fuzzy=False, formatter=None, error=None):
        """
        :type error: 错误
        :return:
        """
        result = super(JSONResponse, self).__call__(fuzzy, error)

        # use formatter function to handler error message
        if formatter and error:
            result = formatter(error.code, error.form_message(fuzzy))

        from flask import make_response  # pylint: disable=import-outside-toplevel
        response = make_response(json.dumps(result))
        response.headers["Content-Type"] = "application/json; charset=utf-8"
        return response


class HTMLResponse(BaseResponse):
    """ 以HTML格式响应出错的情况
    """

    def __call__(self, fuzzy=False, formatter=None, error=None):
        """
        :type error: 错误
        :return:
        """
        result = super(HTMLResponse, self).__call__(fuzzy, error)

        from flask import make_response  # pylint: disable=import-outside-toplevel
        html = '<p>code:%s message:%s</p>' % (result["code"], result["message"])
        if formatter and error:
            html = formatter(error.code, error.form_message(fuzzy))

        response = make_response(html)
        response.headers["Content-Type"] = "text/html; charset=utf-8"
        return response
