from flask import Blueprint,render_template

#error handling methods
errorHandler=Blueprint("errorHandler",__name__)

@errorHandler.app_errorhandler(404)
# @errorHandler.errorhandler(404)
def routenotfound(error):
    error_code="404"
    error_message="page not found"
    return render_template("error.html",code=error_code,message=error_message)

@errorHandler.app_errorhandler(405)
def methodNotallowed(error):
    return render_template("base.html")
