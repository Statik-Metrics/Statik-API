__author__ = 'Gareth Coles'

from bottle import static_file, abort, route, response
from internal.highlight import Highlight


class Routes(object):

    def __init__(self, app, manager):
        self.app = app
        self.highlight = Highlight()
        self.manager = manager

        route("/highlight.css", ["GET", "POST"], self.highlight_css)
        route("/static/<path:path>", ["GET", "POST"], self.static)
        route("/static/", ["GET", "POST"], self.static_403)
        route("/static", ["GET", "POST"], self.static_403)
        route("/.well-known/keybase.txt", ["GET", "POST"],
              self.static_keybase)

    def highlight_css(self):
        response.add_header("Content-Type", "text/css")
        return self.highlight.get_css()

    def static(self, path):
        return static_file(path, root="static")

    def static_403(self):
        abort(403, "You may not list the static files.")

    def static_keybase(self):
        return static_file("keybase.txt", root="static")
