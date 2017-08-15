from flask import Flask

from rule import Rule
import rule


app = Flask(__name__)
app.debug = True


@app.route("/test", methods=['get', 'post'])
def test_handler():
    try:
        params = rule.get_params({"age": Rule(direct_type=int, enum=[1, 2]), "name": Rule()})
    except rule.ParamsValueError as error:
        return error.value

    return str(params)


if __name__ == "__main__":
    app.run()
