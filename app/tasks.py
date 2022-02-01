# from curses.ascii import isalnum, isalpha
from celery import Celery,shared_task
from app.functions.finder import  function_finder
# from config import DevelopmentConfig
from app.util.utility import cmpstring
import time
import json
MONGODB="mongodb://REDACTED_MONGO_URI"
celery_app= Celery(__name__, broker="redis://REDACTED_REDIS_URI",backend="redis://REDACTED_REDIS_URI")
# celery_app.conf.update(celery.co)
@celery_app.task
def lead(**kwargs):
    try:
        print("celery started")
        result=function_finder(kwargs)
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






