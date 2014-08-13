__author__ = 'Gareth Coles'

from bottle import route
from bottle import mako_template as template


class Routes(object):

    def __init__(self, app, manager):
        self.app = app
        self.manager = manager

        route("/", "GET", self.index)

    def index(self):
        # db = self.manager.mongo

        return template(
            "templates/index.html",
            routes=self.manager.api_routes
        )
