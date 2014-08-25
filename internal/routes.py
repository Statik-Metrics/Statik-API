__author__ = 'Gareth Coles'

import json

from bottle import route, request, response
from dicttoxml import dicttoxml

from internal.api import ApiManager
from internal.util import logger

api = ApiManager()


def xml_route(route_, methods=None):
    """Decorator for registering an XML-only API route. It handles
    the content-type header automatically.

    If you're writing two routes with identical code just to support both
    XML and JSON, don't use this, use hybrid_route instead. ::

        @xml_route("routes")
        def routes():
            return {"some": "data"}

    :param route_: String representing the route path
    :param methods: List of methods. Defaults to HTTP GET.
    """

    if methods is None:
        methods = ["GET"]

    def inner(callable_):

        def to_xml(*args, **kwargs):
            response.set_header("Content-Type", "text/xml")

            try:
                return dicttoxml(
                    callable_(*args, **kwargs), custom_root="data"
                )
            except Exception as e:
                logger.exception("Error on route: {0}".format(route_))
                return dicttoxml({"error": str(e)}, custom_root="data")

        route("/<:re:(?i)xml>/{0}".format(route_), methods, to_xml)

    return inner


def json_route(route_, methods=None):
    """Decorator for registering a JSON-only API route. It handles
    the content-type header automatically.

    If you're writing two routes with identical code just to support both
    XML and JSON, don't use this, use hybrid_route instead. ::

        @json_route("routes")
        def routes():
            return {"some": "data"}

    :param route_: String representing the route path
    :param methods: List of methods. Defaults to HTTP GET.
    """

    if methods is None:
        methods = ["GET"]

    def inner(callable_):

        def to_json(*args, **kwargs):
            response.set_header("Content-Type", "application/json")

            try:
                return json.dumps(callable_(*args, **kwargs))
            except Exception as e:
                logger.exception("Error on route: {0}".format(route_))
                return json.dumps({"error": str(e)})

        route("/<:re:(?i)json>/{0}".format(route_), methods, to_json)

    return inner


def hybrid_route(route_, methods=None):
    """Decorator for registering an API route that supports both JSON and XML.
    It handles the content-type header automatically. ::

        @hybrid_route("routes")
        def routes():
            return {"some": "data"}

    :param route_: String representing the route path
    :param methods: List of methods. Defaults to HTTP GET.
    """

    if methods is None:
        methods = ["GET"]

    def inner(callable_):

        def to_json(*args, **kwargs):
            response.set_header("Content-Type", "application/json")

            try:
                return json.dumps(callable_(*args, **kwargs))
            except Exception as e:
                logger.exception("Error on route: {0}".format(route_))
                return json.dumps({"error": str(e)})

        def to_xml(*args, **kwargs):
            response.set_header("Content-Type", "text/xml")

            try:
                return dicttoxml(
                    callable_(*args, **kwargs), custom_root="data"
                )
            except Exception as e:
                logger.exception("Error on route: {0}".format(route_))
                return dicttoxml({"error": str(e)}, custom_root="data")

        def type_dispatch(*args, **kwargs):
            accepts = request.headers.get("accepts", None)

            if accepts == "text/xml":
                return to_xml(*args, **kwargs)
            elif accepts == "application/json":
                return to_json(*args, **kwargs)
            elif accepts is None:
                return "Missing MIME type - please specify it in the " \
                       "\"Accepts\" header."
            else:
                return "Unknown MIME type: {0}".format(accepts)

        route("/<:re:(?i)xml>/{0}".format(route_), methods, to_xml)
        route("/<:re:(?i)json>/{0}".format(route_), methods, to_json)
        route("/<:re:(?i)api>/{0}".format(route_), methods, type_dispatch)

        return lambda: None

    return inner
