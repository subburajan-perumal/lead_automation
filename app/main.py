from flask import Flask
# from app.views.error_handler import errorHandler,badrequest_handler
from app.views.home import home
from app.config import DevelopmentConfig

# import tasks


def create_app():
    app=Flask(__name__)
    app.config.from_object(DevelopmentConfig())
    app.register_blueprint(home)
    # app.register_blueprint(errorHandler)
    # app.register_error_handler(errorHandler,badrequest_handler)
    return app
    
# app=create_app()





    