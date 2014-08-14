__author__ = 'Gareth Coles'

from bottle import route
from bottle import mako_template as template

from internal.api import ApiManager
from internal.util import log


class Routes(object):

    def __init__(self, app, manager):
        self.apis = ApiManager()
        self.app = app
        self.manager = manager

        route("/", "GET", self.index)

    def index(self):
        # db = self.manager.mongo

        return template(
            "templates/index.html",
            apis=self.apis.apis,
            log=log
        )
