from flask import Flask
from views.home import home
from config import DevelopmentConfig
import tasks

app=Flask(__name__)
app.config.from_object(DevelopmentConfig())
app.register_blueprint(home)




if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True, port = 8686,threaded=True)
    