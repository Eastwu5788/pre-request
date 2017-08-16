from flask import Flask
from flask.views import MethodView, View

from rule import Rule, filter_params, Length


app = Flask(__name__)
app.debug = True

field = {
    "age": Rule(direct_type=int, enum=[1, 2]),
    "name": Rule(length=Length(6, 12)),
    "email": Rule(email=True),
    "mobile": Rule(mobile=True),
    "empty": Rule(allow_empty=True, default="sssss_empty")
}

get_field = {
    "year": Rule(direct_type=int, enum=[1920, 1922]),
    "string": Rule(length=Length(6, 12)),
    "email": Rule(email=True),
    "mobile": Rule(mobile=True),
}

post_field = {
    "empty": Rule(allow_empty=True, default="asdf")
}


@app.route("/test", methods=['get', 'post'])
@filter_params(field)
def test_handler(params=None):
    return str(params)


@app.route("/get", methods=['get'])
@filter_params(get=get_field)
def get_handler(params=None):
    return str(params)


@app.route("/post", methods=['post'])
@filter_params(post=post_field)
def post_handler(params=None):
    return str(params)


@app.route("/all", methods=['get', 'post'])
@filter_params(get=get_field, post=post_field)
def all_handler(params=None):
    return str(params)


# 方法视图
class GetView(MethodView):

    @filter_params(get=get_field, response='json')
    def get(self, params=None):
        return str(params)

    @filter_params(post=post_field, response='html')
    def post(self, params=None):
        return str(params)


# 标准视图demo
class BaseView(View):

    @filter_params(get=get_field, post=post_field, response='html')
    def dispatch_request(self, params=None):
        return str(params)


app.add_url_rule('/getview', view_func=GetView.as_view('getview'))
app.add_url_rule('/baseview', view_func=BaseView.as_view('baseview'))


if __name__ == "__main__":
    app.run()
