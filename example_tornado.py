import tornado.httpserver
import tornado.ioloop
import tornado.web

from pre_request.tornado import filter_params
from pre_request.filter_rules import Rule, Length

get_filed = {
    "age": Rule(direct_type=int, enum=[1920, 1930]),
    "mobile": Rule(mobile=True),
    "email": Rule(email=True),
    "string": Rule(length=Length(6, 10)),
    "empty": Rule(allow_empty=True, default="empty_default_value")
}

post_field = {
    "year": Rule(direct_type=int, enum=[1, 2]),
    "test": Rule(allow_empty=True, default="sas_sdf", length=Length(3, 10))
}


class MainTestHandler(tornado.web.RequestHandler):

    @filter_params(get=get_filed, response="html")
    def get(self, params=None):
        self.write(str(params))

    @filter_params(post=post_field, response="html")
    def post(self, params=None):
        self.write(str(params))


def make_app():
    new_app = tornado.web.Application(
        [
            (r"/test", MainTestHandler),
        ],
        debug=True,
    )
    return new_app


if __name__ == "__main__":
    app = make_app()
    server = tornado.httpserver.HTTPServer(app)
    server.bind(8000)
    server.start()
    tornado.ioloop.IOLoop.current().start()
