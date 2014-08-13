__author__ = 'Gareth Coles'

import logging
import os
import yaml

from bottle import run, default_app, request, hook

from internal.db import Db
from internal.schemas import schemas
from internal.singleton import Singleton
from internal.util import log_request, log


class Manager(object, metaclass=Singleton):

    db = {}
    mongo_conf = {}
    mongo = None

    def __init__(self):
        self.app = default_app()

        self.mongo_conf = os.environ.get("MONGOHQ_URL", None)

        if not self.mongo_conf:
            self.db = yaml.load(open("config/database.yml", "r"))
            self.mongo_conf = self.db["mongo"]

        self.setup_mongo()

        self.routes = {}
        self.api_routes = {}

        files = os.listdir("routes")
        files.remove("__init__.py")

        for _file in files:
            if _file.endswith(".py"):
                module = _file.rsplit(".", 1)[0]
                try:
                    log(
                        "Loading routes module '{0}'".format(module),
                        logging.INFO
                    )
                    mod = __import__(
                        "routes.{0}".format(module),
                        fromlist=["Routes"]
                    )
                    self.routes[module] = mod.Routes(self.app, self)
                except Exception as e:
                    log(
                        "Error loading routes module '{0}': {1}"
                        .format(module, e)
                    )

        log("{0} routes set up.".format(len(self.app.routes)))

    def add_api_route(self,
                      route: "Human-readable route path",
                      description: "Description for the index page"):

        if route in self.api_routes:
            return False

        self.api_routes[route] = description
        return True

    def get_app(self):
        return self.app

    def setup_mongo(self):
        try:
            self.mongo = Db(self.mongo_conf)
            self.mongo.setup()

            for key in schemas.keys():
                log("Adding schema for collection: {0}".format(key))
                self.mongo.add_schema(key, schemas[key])

            self.mongo.client.admin.command("ping")
            log("Set up Mongo successfully.")
        except Exception as e:
            log("Unable to set up Mongo: {0}".format(e), logging.ERROR)

    def start(self):
        def log_all():
            log_request(
                request,
                "{0} {1} ".format(request.method, request.fullpath)
            )

        hook('after_request')(log_all)

        try:
            config = yaml.load(open("config/development.yml", "r"))
            host = config.get("host", "127.0.0.1")
            port = config.get("port", 8080)
            server = config.get("server", "cherrypy")
        except Exception as e:
            log("Unable to load development config: {0}".format(e))
            log("Continuing using the defaults.")
            host = "127.0.0.1"
            port = 8080
            server = "cherrypy"

        run(app=self.get_app(), host=host, port=port, server=server)
