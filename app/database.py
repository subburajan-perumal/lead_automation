from flask_pymongo import PyMongo
from pymongo import MongoClient

from config import Config

mongo = PyMongo()

_client = None


def get_db():
    """Database handle for code running outside a Flask request (Celery tasks, automators).

    One MongoClient per process: pymongo pools connections itself, so creating a
    client per lead only leaks sockets.
    """
    global _client
    if _client is None:
        if not Config.MONGO_URI:
            raise RuntimeError("MONGO_URI is not set. Copy .env.example to .env and fill it in.")
        _client = MongoClient(Config.MONGO_URI)
    return _client[Config.MONGO_DB_NAME]
