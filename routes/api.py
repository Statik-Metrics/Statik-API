__author__ = 'Gareth Coles'

from bottle import route
from internal.highlight import Highlight


class Routes(object):

    def __init__(self, app, manager):
        self.app = app
        self.highlight = Highlight()
        self.manager = manager

        route("/json", "GET", self.api_index)

        self.manager.add_api_route(
            "GET /test/<test variable>",
            """A test route. Doesn't actually exist, just here for
            illustration purposes.
            """
        )

        self.manager.add_api_route(
            "GET /json",
            """<p> The list of routes in JSON format.
    You could use this for service or capability discovery, for example.
</p>

<div class="ui horizontal icon divider">
    <i class="circular code icon"></i>
</div>

{0}
            """.format(self.highlight.highlight("""
{
    "routes": {
        "GET /test/<test variable>": "A test route.",
        "GET /json": "The list of routes in JSON format. You could use this
                      for service or capability discovery, for example."
    }
}
            """, "json"))
        )

    def api_index(self):
        return {"routes": self.manager.api_routes}
