"""
This module contain the flask  webpages and error handling site
and creata a app
"""
from flask import Flask
# from app.views.error_handler import errorHandler,badrequest_handler
from app.views.home import home
from app.views.error_handler import errorHandler
from app.config import DevelopmentConfig
from app.views.site import site
# import tasks


def create_app():
    """_summary_
    This is a function create a flask app
    Returns:
        class: return a flask class
    """
    app=Flask(__name__)
    app.config.from_object(DevelopmentConfig())
    app.register_blueprint(home)
    app.register_blueprint(errorHandler)
    app.register_blueprint(site)
    # app.register_error_handler(errorHandler,badrequest_handler)
    return app
