__author__ = 'Gareth Coles'

import dicttoxml

from bottle import route, response

from internal.api import ApiManager
from internal.highlight import Highlight
from internal.util import log


class Routes(object):

    def __init__(self, app, manager):
        self.apis = ApiManager()
        self.app = app
        self.highlight = Highlight()
        self.manager = manager

        route("/<:re:(?i)json>/routes", "GET", self.json_routes)
        route("/<:re:(?i)xml>/routes", "GET", self.xml_routes)

        r = self.apis.add_route(
            "/test/[test variable]",
            "GET",
            "A test route",
            "test"
        )

        log("Result: {0}".format(r))

        r = self.apis.add_route(
            "/routes",
            "GET",
            "The list of routes in a computer-readable format",
            "routes"
        )

        log("Result: {0}".format(r))

    def json_routes(self):
        routes = {}
        for k in self.apis.apis.keys():
            done = {}

            for kk in self.apis.apis[k].keys():
                done[kk] = self.apis.apis[k][kk]["text"]

            routes[k] = done

        return {"routes": routes}

    def xml_routes(self):
        routes = {}
        for k in self.apis.apis.keys():
            done = {}

            for kk in self.apis.apis[k].keys():
                done[kk] = self.apis.apis[k][kk]["text"]

            routes[k] = done

        response.set_header("Content-Type", "text/xml")
        return dicttoxml.dicttoxml({"routes": routes}, custom_root="data")
