__author__ = 'Gareth Coles'

import pymongo

from internal.singleton import Singleton


class Db(object, metaclass=Singleton):
    """
    Very, very simple schema validation. Super simple.

    This introduces a singleton for managing the Mongo instance. It exposes
    `client` and `db` objects, for direct access to the Mongo classes,
    as well as `add_schema(collection, schema)` and
    `get_collection(collection)`.

    If you're using Mongo, you should define schemas for each collection you
    are using. This ensures that you're not inserting documents that are
    structured incorrectly.

    Note that schema validation is only done on insert and update, not
    find and other collection functions. This also means that you can only
    update entire documents, using the $set operator won't work.

    Your schema should be a simple dictionary. As documents can also be
    considered dictionaries, this makes validation easier. Let's say we
    have a document similar to the following::

        {
            "title": "Hello, world!",
            "text": "This is my first post!",
            "tags": ["first", "post", "whee"],
            "when": datetime.datetime.utcnow()
        }

    Our schema might look like the following::

        {
            "title": Type(str),
            "text": Type(str),
            "tags": Type(list),
            "when": Type(datetime.datetime)
        }

    Schemas check three things:
    * That all the keys in the schema are present in the document
    * That the types specified in the schema match the data in the document
    * That the document doesn't have any extra keys

    If your documents don't fulfill these three checks, then ValidationError
    will be raised. For example, the following three documents will fail
    the check. ::

        {
            "title": "My second post.",
            "text": "Have another post!",
            "tags": "mongo,is,awesome",  # Not a list
            "when": datetime.datetime.utcnow()
        }

        {
            "title": "My second post.",
            "text": "Have another post!",
            # Missing the "tags" key
            "when": datetime.datetime.utcnow()
        }

        {
            "title": "My second post.",
            "text": "Have another post!",
            "tags": ["mongo", "is", "awesome"],
            "when": datetime.datetime.utcnow(),
            "author": "me"  # Extra key
        }

    This is a /very/ simple schema validation method, but it should be
    sufficient for most cases. If you feel as if other people may be inserting
    data, or you're doing it manually, you should use something like Ming the
    Merciless.
    """

    client = None
    db = None
    schemas = {}
    uri = ""

    def __init__(self, config):
        self.config = config

    def setup(self):
        if self.client is not None and self.db is not None:
            raise AlreadySetUpError("MongoDB has already been configured.")

        if self.config.get("default", True):
            client = pymongo.MongoClient()
            db = client.archivesmc
            self.uri = "mongodb://localhost/statik"
        else:
            auth = self.config.get("authentication", None)

            if auth is None:
                uri = "mongodb://{0}:{1}/{2}".format(
                    self.config["host"],
                    self.config["port"],
                    self.config["db"]
                )
            else:
                uri = "mongodb://{0}:{1}@{2}:{3}/{4}".format(
                    auth["username"],
                    auth["password"],
                    self.config["host"],
                    self.config["port"],
                    self.config["db"]
                )

            client = pymongo.MongoClient(uri)
            db = client[self.config["db"]]
            self.uri = uri

        self.client = client
        self.db = db

    def add_schema(self, collection, schema):
        self.schemas[collection] = schema

    def get_collection(self, collection):
        return Collection(self.db[collection],
                          self.schemas.get(collection, None))


class Collection(object):
    coll = None
    schema = None

    def __init__(self, collection, schema):
        self.coll = collection
        self.schema = schema

    def __getattribute__(self, item):
        try:
            # Check whether we defined our own methods
            return super(Collection, self).__getattribute__(self, item)
        except AttributeError:
            # If not, check if they exist on the collection
            return self.coll.__getattribute__(item)

    def insert(self, data):
        if self.schema is None:
            return self.coll.insert(data)

        for key in self.schema.keys():
            if key not in data:
                raise ValidationError("Missing key: {0}".format(key))

            if not self.schema[key].validate(data[key]):
                raise ValidationError("Key {0} is not in type list {1}".format(
                    key, self.schema[key].types
                ))

        for key in data:
            if key not in self.schema:
                raise ValidationError("Extra key: {0}".format(key))

        return self.coll.insert(data)

    def update(self, criteria, data, *args, **kwargs):
        if self.schema is None:
            return self.coll.update(criteria, data, *args, **kwargs)

        for key in self.schema.keys():
            if key not in data:
                raise ValidationError("Missing key: {0]".format(key))

            if not isinstance(data[key], self.schema[key]):
                raise ValidationError("Key {0} is not of type {1}".format(
                    key, self.schema[key]
                ))

        for key in data:
            if key == "_id":
                continue

            if key not in self.schema:
                raise ValidationError("Extra key: {0}".format(key))

        return self.coll.update(criteria, data, *args, **kwargs)


class AlreadySetUpError(Exception):
    pass


class ValidationError(Exception):
    pass
