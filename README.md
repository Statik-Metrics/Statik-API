Statik API
==========

This is the API server for Statik. It's designed to be the public-facing
stats querying server, plus a form of API documentation.

This server is live at [api.statik.io][http://api.statik.io/].

Requirements
------------

To use this, you'll need the following.

* Python 3.4 or later
* The following Python libraries
    * bottle
    * mako
    * pymongo
    * pyyaml
* To run the development server, you'll need one of the
[supported Bottle backends](http://bottlepy.org/docs/dev/deployment.html#switching-the-server-backend).
    We suggest CherryPy.

Setting up
----------

* Install Python 3.4 or later if you haven't already
* Install the required libraries - You can do this quickly using `pip install -r requirements.txt`
* Enter the `config/` folder
    * Copy `config.yml.example` to `config.yml` and fill it out.
    * Copy `database.yml.example` to `database.yml` and fill it out.
    * You can also do `development.yml.example` if you need to change the defaults for local testing.
* Launch the server
    * For testing, you can simply run `python run.py` or `python3 run.py`.
    * For production, you should *really* use uWSGI.

Development
-----------

If you're going to work on this or are considering submitting a pull request, please
take note of the following guidelines.

* This project fully adheres to PEP8. [Go read it](http://legacy.python.org/dev/peps/pep-0008/).
    * Our code is tested using the Flake8 tool. If your code doesn't adhere to PEP8, it will fail the tests.
    * The following exceptions are allowed:
        * Anything about maximum complexity
        * F841: Local variables assigned but never used
        * T000: TODO notes
        * F403: `from module import *`
        * E265: Block comment not starting with `# ` (Note the space)
* If you're creating an API route, you *must* provide the route itself and a description
    to the manager's `add_api_route` method.
