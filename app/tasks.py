# from curses.ascii import isalnum, isalpha
from unittest import result
from celery import Celery
from app.functions.finder import  function_finder
from app.config import DevelopmentConfig
from app.functions.leadautomator import LeadAutomator
# from app.util.utility import cmpstring
import time
import json
import os

MONGODB="mongodb://REDACTED_MONGO_URI"
celery_app= Celery(__name__, broker="redis://REDACTED_REDIS_URI",backend="redis://REDACTED_REDIS_URI")
# celery_app.conf(DevelopmentConfig())
# celery_app.conf.update(celery.co)

@celery_app.task
def lead(**lead_data):
    try:
        # print(os.getenv())
        print("celery started")
        result=function_finder(lead_data)
        # lead_sender=LeadAutomator(lead_data)
        # lead_sender.create_lead()
        # lead_sender.generate_lead("enquired")
        # lead_sender.generate_lead("interested")
        # lead_sender.generate_lead("location")
        result="success"
    
        return result
    except:
        return "failed"

@celery_app.task
def bulk_lead(*args):
    try:
        # f = open("bulk_lead.json","a")
        # f.write(str(args))
        # f.close()
        # time.sleep(10)
        return "success" 
    except:
        return "failed"






