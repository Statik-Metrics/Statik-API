__author__ = 'Gareth Coles'

from bottle import route


class Routes(object):

    def __init__(self, app, manager):
        self.app = app
        self.manager = manager

        route("/json", "GET", self.api_index)

        self.manager.add_api_route(
            "GET /test/<test variable>",
            "A test route."
        )

        self.manager.add_api_route(
            "GET /json",
            "The list of routes in JSON format"
        )

    def api_index(self):
        return {"routes": self.manager.api_routes}
