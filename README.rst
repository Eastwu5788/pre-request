.. raw:: html

    <p align="center">
        <a href="#readme">
            <img alt="Pre-request logo" src="https://pre-request.readthedocs.io/en/master/_images/logo.jpg">
        </a>
    </p>
    <p align="center">
        <a href="https://github.com/Eastwu5788/pre-request/actions/workflows/intergration.yml"><img alt="CI" src="https://github.com/Eastwu5788/pre-request/actions/workflows/intergration.yml/badge.svg"></a>
        <a href="https://codecov.io/gh/Eastwu5788/pre-request"><img alt="Coveralls" src="https://codecov.io/gh/Eastwu5788/pre-request/branch/master/graph/badge.svg?token=KAB3VL6B7J"></a>
        <a href="https://github.com/Eastwu5788/pre-request/blob/master/LICENSE"><img alt="License" src="https://img.shields.io/pypi/l/pre-request?color=brightgreen"></a>
        <a href="https://pre-request.readthedocs.io/en/master/"><img alt="Docs" src="https://readthedocs.org/projects/pre-request/badge/?version=master"></a>
        <a href="https://pypi.org/project/pre-request/"><img alt="PyPI" src="https://img.shields.io/pypi/v/pre-request?color=brightgreen"></a>
        <a href="https://gitter.im/pre-request/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge"><img alt="IM" src="https://badges.gitter.im/pre-request/community.svg"/></a>
    </p>


========

This framework is designed to validate request params for `Flask` web framework.

It has the following `unique` features:

* Cross Field and Cross Struct validations
* Array and Map diving, which allows any or all levels of a multidimensional field to be validated
* Customizable error response


Install
-----------

you can simply install it by PyPi:

::

    pip install pre-request


Document
----------

`pre-request` manual could be found at: https://pre-request.readthedocs.io/en/master/index.html


A Simple Example
------------------

This is very easy to use `pre-request` in your project

.. code-block:: python

   from flask import Flask

   from pre_request import pre, Rule

   app = Flask(__name__)

   args = {
      "userId": Rule(type=int, required=True)
   }

   @app.route("/")
   @pre.catch(args)
   def hello_world(params):
      from flask import g
      return str(params == g.params)

what happened in this code ?

1. Use `pre-request` library to import a global object `pre`
2. Define request params rule, e.g. `userId` must be type of `int` and required
3. Use `@pre.catch(req_params)` to filter input value
4. Use `~flask.g` or `def hello_world(params)` to get formatted input value。


Complex Example
-----------------

We use a very complex example to show the powerful of this framework. Otherwise you can find amount of examples at: `https://github.com/Eastwu5788/pre-request/tree/master/examples`

.. code-block:: python

    from flask import Flask
    from pre_request import pre, Rule

    args = {
        "userFirst": {
            "userId": Rule(type=int, required=False),
            "socialInfo": {
                "gender": Rule(type=int, enum=[1, 2], default=1),
                "age": Rule(type=int, gte=18, lt=80),
                "country": Rule(required=True, deep=False)
            }
        },
        "userSecond": {
            "userId": Rule(type=int, required=False, neq_key="userFirst.userId"),
            "friends": Rule(type=dict, required=True, multi=True, structure={
                "userId": Rule(type=int, required=True, dest="user_id"),
                "userName": Rule(type=str, required=True, dest="user_name")
            })
        }
    }


    app = Flask(__name__)
    app.config["TESTING"] = True
    client = app.test_client()

    @app.route("/structure", methods=["GET", "POST"])
    @pre.catch(args)
    def structure_handler(params):
        return str(params)


    if __name__ == "__main__":
        resp = app.test_client().post("/structure", json={
            "userFirst": {
                "userId": "13",
                "socialInfo": {
                    "age": 20,
                }
            },
            "userSecond": {
                "userId": 14,
                "friends": [
                    {
                        "userId": 13,
                        "userName": "Trump"
                    }
                ]
            },
            "country": "CN",
            "userFirst.socialInfo.gender": 1
        })

        print(resp.get_data(as_text=True))


Use parse
-------------

We can use function `pre.parse` instead of decorator `@pre.catch()`

.. code-block:: python

    args = {
        "params": Rule(email=True)
    }

    @app.errorhandler(ParamsValueError)
    def params_value_error(e):
        return pre.fmt_resp(e)


    @app.route("/index")
    def example_handler():
        rst = pre.parse(args)
        return str(rst)


Contributing
--------------

How to make a contribution to Pre-request, see the `contributing`_.

.. _contributing: https://github.com/Eastwu5788/pre-request/blob/master/CONTRIBUTING.rst


Coffee
---------

Please give me a cup of coffee, thank you!

BTC: 1657DRJUyfMyz41pdJfpeoNpz23ghMLVM3

ETH: 0xb098600a9a4572a4894dce31471c46f1f290b087


Links
------------
* Documentaion: https://pre-request.readthedocs.io/en/master/index.html
* Release: https://pypi.org/project/pre-request/
* Code: https://github.com/Eastwu5788/pre-request
* Issue tracker: https://github.com/Eastwu5788/pre-request/issues
* Test status: https://coveralls.io/github/Eastwu5788/pre-request
