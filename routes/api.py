__author__ = 'Gareth Coles'

from internal.api import ApiManager
from internal.routes import hybrid_route


class Routes(object):

    def __init__(self, app, manager):
        self.apis = ApiManager()
        self.app = app
        self.manager = manager
        self.db = self.manager.mongo

        self.apis.add_route(
            "/routes",
            "GET",
            "The list of routes in a computer-readable format",
            "routes"
        )

        self.apis.add_route(
            "/servers",
            "GET",
            "The total number of entries in the data collection",
            "servers"
        )

        # This will register it and ensure the returned types are correct.
        hybrid_route("routes")(self.routes)
        hybrid_route("servers")(self.count_servers)

    def routes(self):
        routes = {}
        for k in self.apis.apis.keys():
            done = {}

            for kk in self.apis.apis[k].keys():
                done[kk] = self.apis.apis[k][kk]["text"]

            routes[k] = done

        return {"routes": routes}

    def count_servers(self):
        data = self.db.get_collection("data")
        servers = data.count()

        return {"servers": servers}
