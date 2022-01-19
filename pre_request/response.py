# -*- coding: utf-8 -*-
import typing as t
import json
# check
if t.TYPE_CHECKING:
    from flask import Response  # pylint: disable=unused-import
    from .exception import ParamsValueError  # pylint: disable=unused-import


class BaseResponse:
    """ PreRequest basic response class
    """

    @staticmethod
    def fmt_result(error: "ParamsValueError", fuzzy: bool = False) -> dict:
        message = "parameter validate failed" if fuzzy else error.message
        return {"respCode": 400, "respMsg": message, "result": {}}

    @classmethod
    def make_response(
            cls,
            error: "ParamsValueError",
            fuzzy: bool = False,
            formatter: t.Optional[t.Callable] = None
    ) -> "Response":
        raise NotImplementedError()


class JSONResponse(BaseResponse):
    """ Handler response with json format
    """

    @classmethod
    def make_response(
            cls,
            error: "ParamsValueError",
            fuzzy: bool = False,
            formatter: t.Optional[t.Callable] = None
    ) -> "Response":
        result = cls.fmt_result(error, fuzzy)

        # use formatter function to handler error message
        if formatter and error:
            result = formatter(error)

        from flask import make_response  # pylint: disable=import-outside-toplevel
        response = make_response(json.dumps(result))
        response.headers["Content-Type"] = "application/json; charset=utf-8"
        return response


class HTMLResponse(BaseResponse):
    """ Handler response with html format
    """

    @classmethod
    def make_response(
            cls,
            error: "ParamsValueError",
            fuzzy: bool = False,
            formatter: t.Optional[t.Callable] = None
    ) -> "Response":
        result = cls.fmt_result(error, fuzzy)

        from flask import make_response  # pylint: disable=import-outside-toplevel
        html = f'<p>code:{result["code"]} message:{result["message"]}</p>'
        if formatter and error:
            html = formatter(error)

        response = make_response(html)
        response.headers["Content-Type"] = "text/html; charset=utf-8"
        return response
