"""
This module contain the flask  webpages and error handling site
and creata a app
"""

from app.database import mongo
from flask import Flask
from app.views.home import home
from app.views.error_handler import errorHandler
from config import config
from app.views.site import site
from app.views.lead import lead
# One Celery app for the whole project, so `-A app.celery` and `-A app.tasks` start the same workers.
from app.tasks import celery_app as celery  # noqa: F401
import logging
import os
logging.basicConfig(level=logging.DEBUG)


def create_app(config_name=None):

    """_summary_
    This is a function create a flask app
    Returns:
        class: return a flask class
    """

    if config_name is None:
        config_name = os.getenv("FLASK_CONFIG", "development")
    app = Flask(__name__)

    app.config.from_object(config[config_name])
    if not app.config["TESTING"]:
        config[config_name].validate()
    app.logger.info("Lead Automation App created ")
    mongo.init_app(app)
    app.register_blueprint(home)
    app.register_blueprint(errorHandler)
    app.register_blueprint(site)
    app.register_blueprint(lead)
    return app
