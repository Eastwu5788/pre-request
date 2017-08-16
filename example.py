from flask import Flask

from rule import Rule,filter_params, Length
import rule


app = Flask(__name__)
app.debug = True

field = {
    "age": Rule(direct_type=int, enum=[1, 2]),
    "name": Rule(length=Length(6, 12)),
    "email": Rule(email=True),
    "mobile": Rule(mobile=True),
    "empty": Rule(allow_empty=True, default="sssss_empty")
}


@app.route("/test", methods=['get', 'post'])
@filter_params(field)
def test_handler(params=None):
    return str(params)


if __name__ == "__main__":
    app.run()
