from flask import Blueprint,render_template

#error handling methods
errorHandler=Blueprint("errorHandler",__name__)

@errorHandler.app_errorhandler(404)
# @errorHandler.errorhandler(404)
def routenotfound(error):
    return "route not found", 404

@errorHandler.app_errorhandler(405)
def methodNotallowed(error):
    return render_template("base.html")