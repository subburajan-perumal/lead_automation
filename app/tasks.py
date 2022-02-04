# from curses.ascii import isalnum, isalpha
from celery import Celery
from app.functions.finder import  function_finder
from app.config import DevelopmentConfig
# from app.util.utility import cmpstring
import time
import json
MONGODB="mongodb://REDACTED_MONGO_URI"
celery_app= Celery(__name__, broker="redis://REDACTED_REDIS_URI",backend="redis://REDACTED_REDIS_URI")
# celery_app.conf(DevelopmentConfig())
# celery_app.conf.update(celery.co)

@celery_app.task
def lead(**lead_data):
    try:
        print("celery started")
        result=function_finder(lead_data)
        return result
    except:
        return "failed"

@celery_app.task
def bulk_lead(*args):
    try:
        f = open("bulk_lead.json","a")
        f.write(str(args))
        f.close()
        time.sleep(10)
        return "success" 
    except:
        return "failed"






