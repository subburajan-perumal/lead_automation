from config import Config
bind= "0.0.0.0:5000"
workers= 2
accesslog= Config.LOG_PATH+"gunicorn.log"
wsgi_app= "run:app"
access_log_format='%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
errorlog= Config.LOG_PATH+"gunicorn_error.log"
loglevel="debug"
# proc_name="lead_automation_server"
ssl=""
certfile=""
capture_output= True