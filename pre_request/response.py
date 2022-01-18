# -*- coding: utf-8 -*-
import json


class BaseResponse:
    """ PreRequest basic response class
    """

    def __call__(self, fuzzy=False, error=None):
        """ Use __call__ function to generate response

        :param error: error
        :type error: ParamsValueError
        """
        if error:
            self.error = error

        return {"respCode": self.error.code, "respMsg": self.error.form_message(fuzzy), "result": {}}


class JSONResponse(BaseResponse):
    """ Handler response with json format
    """

    def __call__(self, fuzzy=False, formatter=None, error=None):
        """ Use __call__ function to generate response

        :type error: special error
        """
        result = super().__call__(fuzzy, error)

        # use formatter function to handler error message
        if formatter and error:
            result = formatter(error.code, error.form_message(fuzzy))

        from flask import make_response  # pylint: disable=import-outside-toplevel
        response = make_response(json.dumps(result))
        response.headers["Content-Type"] = "application/json; charset=utf-8"
        return response


class HTMLResponse(BaseResponse):
    """ Handler response with html format
    """

    def __call__(self, fuzzy=False, formatter=None, error=None):
        """ Use __call__ function to generate response

        :type error: special error
        """
        result = super().__call__(fuzzy, error)

        from flask import make_response  # pylint: disable=import-outside-toplevel
        html = f'<p>code:{result["code"]} message:{result["message"]}</p>'
        if formatter and error:
            html = formatter(error.code, error.form_message(fuzzy))

        response = make_response(html)
        response.headers["Content-Type"] = "text/html; charset=utf-8"
        return response
