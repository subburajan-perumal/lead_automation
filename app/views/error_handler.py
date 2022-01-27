from flask import Blueprint

#error handling methods
errorHandler=Blueprint("errorHandler",__name__)
@errorHandler.errorhandler(Exception)
def badrequest_handler(e):
        return "an Error occured"+str(e),404