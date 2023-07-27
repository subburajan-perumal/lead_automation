import os

from config import Config

os.makedirs(Config.LOG_PATH, exist_ok=True)

bind = os.getenv("GUNICORN_BIND", "0.0.0.0:5000")
workers = 1
accesslog = os.path.join(Config.LOG_PATH, "gunicorn.log")
wsgi_app = "run:app"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
errorlog = os.path.join(Config.LOG_PATH, "gunicorn_error.log")
loglevel = os.getenv("GUNICORN_LOGLEVEL", "info")
proc_name = "lead_automation_server"
capture_output = True
keepalive = 120
timeout = 600
worker_class = "gthread"
threads = 3
