"""
This module contain the flask  webpages and error handling site
and creata a app
"""

from app.database import mongo
from flask import Flask
from celery import Celery
from app.views.home import home
from app.views.error_handler import errorHandler
from config import config
from config import CeleryConfig
from app.views.site import site
from app.views.lead import lead
import logging
import os
logging.basicConfig(level=logging.DEBUG)

celery = Celery(__name__,
                broker=CeleryConfig.BROKER_URL,
                result_backend=CeleryConfig.RESULT_BACKEND)


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
    app.logger.info("Lead Automation App created ")
    # app.config.from_object(config[config_name])
    mongo.init_app(app)
    app.register_blueprint(home)
    app.register_blueprint(errorHandler)
    app.register_blueprint(site)
    app.register_blueprint(lead)
    return app
