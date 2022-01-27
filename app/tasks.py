from app.config import DevelopmentConfig
from celery import Celery
import time
from pymongo import MongoClient
import json


CELERY= Celery("tasks", broker=DevelopmentConfig.broker_url,backend=DevelopmentConfig.result_backend)

@CELERY.task
def lead(**kwargs):
    try:
        f = open("test.json",'a')

        f.write(json.dumps(kwargs))
        f.close()
        # time.sleep(10)
        
        return "success"
    except:
        return "failed"

@CELERY.task
def bulk_lead(*args):
    try:
        f = open("bulk_lead.json","a")
        f.write(str(args))
        f.close()
        return "success" 
    except:
        return "failed"






