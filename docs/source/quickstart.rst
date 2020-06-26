Quickstart
===============

Eager to get started? This page gives a good example to use pre-request. It assumes you already have pre-request installed
If you do not, head over to the Installation section.

Minimal Example
----------------

A minimal example looks something like this:

.. code-block:: python

   from flask import Flask

   from pre_request import pre
   from pre_request import Rule

   app = Flask(__name__)

   req_params = {
      "userId": Rule(type=int, required=True)
   }

   @app.route("/")
   @pre.catch(req_params)
   def hello_world(params):
      return str(params)


what happened in this code ?

1. Use `pre-request` library to import a global object `pre`
2. Define request params rule, `userId` must be type of `int` and required
3. Use `@pre.catch(req_params)` to filter input value
4. Use `~flask.g` or `def hello_world(params)` to get formatted input value。


`pre` singleton
----------------

pre-request support global singleton object, we can use this object to update runtime params

-  `pre.fuzzy` pre-request will fuzzy error message to avoid expose sensitive information
-  `pre.sore_key` use another params to store formatted request info
-  `pre.content_type` pre-request will response html or json error message, use `application/json` or `text/html`
-  `pre.skip_filter` pre-request will ignore all of the check filter, but `dest` is still valid.

`Flask` Extension
------------------

pre-request support flask extension configuration to load params.


.. code-block:: python

   app = Flask(__name__)

   app.config["PRE_FUZZY"] = True
   app.config["PRE_STORE_KEY"] = "pp"
   app.config["PRE_CONTENT_TYPE"] = "application/json"
   app.config["PRE_SKIP_FILTER"] = False

   pre.init_app(app=app)


use decorator
--------------

pre-request use decorator `pre.catch` to validate request params with special kind of method


.. code-block:: python

    @app.route("/get", methods=['get'])
    @pre.catch(get=req_params)
    def get_handler(params):
        return str(params)

    @app.route("/post", methods=['post'])
    @pre.catch(post=req_params)
    def get_handler(params):
        return str(params)

we can also support validate different rule for different request params

.. code-block:: python

    @app.route("/all", methods=['get', 'post'])
    @pre.catch(get=get_field, post=post_field)
    def all_handler(params):
        return str(params)


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
