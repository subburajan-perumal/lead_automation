"""
This module contain the flask  webpages and error handling site
and creata a app
"""
from flask import Flask
from flask_pymongo import PyMongo
from celery import Celery
import sentry_sdk
from app.tasks import make_celery
from app.views.home import home
from app.views.error_handler import errorHandler
from config import config
from config import CeleryConfig
from app.views.site import site
import logging
import os
from sentry_sdk.integrations.celery import CeleryIntegration  
# import tasks
logging.basicConfig(level=logging.DEBUG)

celery=Celery(__name__, broker=CeleryConfig.BROKER_URL, result_backend=CeleryConfig.RESULT_BACKEND)

sentry_sdk.init(dsn="https://redacted@example.com/6320262",integrations=[CeleryIntegration()],traces_sample_rate=1.0)

def create_app(config_name=None):

    """_summary_
    This is a function create a flask app
    Returns:    
        class: return a flask class
    """

    if config_name is None:
        # print("app created with none config")
        config_name = os.getenv("FLASK_CONFIG","development")
    # else:print("app create with class")
    app=Flask(__name__)
    # print(__name__)
    app.config.from_object(config[config_name])
    app.logger.info("Lead Automation App created ")
    # celery=make_celery(app)
    # celery.conf.update(app.config)
    # print(app.config)
    # print(celery.conf)
    # mongo=PyMongo(app)
    # celery_app=make_celery(app)
    
    app.config.from_object(config[config_name])
    app.register_blueprint(home)
    app.register_blueprint(errorHandler)
    app.register_blueprint(site)
    # app.register_error_handler(errorHandler,badrequest_handler)
    return app

def configure_logging(app):
    pass

