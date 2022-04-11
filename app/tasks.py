from unittest import result
from celery import Celery
from config import CeleryConfig
from config import keyword_field
from celery import shared_task,group
from bson import json_util,ObjectId

from celery import group
# from app.functions.finder import  function_finder
from app.functions.leadautomator import LeadAutomator
from app.functions.site_base import SiteAutomator
import time
import json
import os

# MONGODB="mongodb://REDACTED_MONGO_URI"
celery_app= Celery(__name__, broker=CeleryConfig.BROKER_URL,backend=CeleryConfig.RESULT_BACKEND)
# celery_app.conf(DevelopmentConfig())
# celery_app.conf.update(celery.co)

@celery_app.task(name="app.tasks.check")
def check_celery():
    print("celery working")

@celery_app.task
def lead(**lead_data):
        # lead_sender=LeadAutomator(lead_data)
        # lead_sender.create_lead()
        # lead_sender.generate_lead("enquired")
        # lead_sender.generate_lead("interested")
        # lead_sender.generate_lead("location")
    try:
        # print(os.getenv())
        print("celery started")
        # result=function_finder(lead_data)
        LA=LeadAutomator(lead_data=lead_data)
        LA.create_lead()
        for _ in keyword_field:
            LA.get_keywords(lead_data.get(_["field"],""),";")

        # LA.get_keywords()
        # LA.get_keywords(lead_data.get("project_enquired_for",""),";")
        # LA.get_keywords(lead_data.get("interested_project",""),";")
        # LA.get_keywords(lead_data.get("interested_localities",""),";")
        LA.get_keywords("None (default)",";")
        site_list=LA.search_by_keyword()
        site_list= json.loads(json_util.dumps(site_list))
        print(site_list)
        task_list=[]

        # print(loads(dumps(site_list)))
        for _site in site_list:
            site_name = _site['name']
            site_projectname = _site['project_list']['project_name']
            task_list.append(browserAutomate.s(_site,lead_data))
            # browserAutomation = SiteAutomator(lead_data["phone"],
            #                             lead_data["email"],
            #                             lead_data,
            #                             site_data=_site)
            # browserAutomation.projectCheck(site_name, site_projectname)
            # browserAutomation.automated_flow()
            # browserAutomation.upload_data()
            # browserAutomation.teardown()
            
            # celery_app.task.browserAutomate(site,lead_data)
        job=group(task_list)
        output=job.apply_async(queue="browser")
        print(output)
        result="success"
    
        return result
    except Exception as e:
        print(str(e))
        return "failed"

# @celery_app.task
@shared_task
def browserAutomate(_site,lead_data):
    print("automation working")
    site_name = _site['name']
    site_projectname = _site['project_list']['project_name']
    browserAutomation = SiteAutomator(lead_data["phone"],
                                        lead_data["email"],
                                        lead_data,
                                        site_data=_site)
    browserAutomation.projectCheck(site_name, site_projectname)
    browserAutomation.automated_flow()
    upload_result=browserAutomation.upload_data()
    print(f"data upload :{upload_result}")
    browserAutomation.teardown()
    return upload_result


@shared_task
# @celery_app.task
def bulk_lead(*args):
    try:
        # f = open("bulk_lead.json","a")
        # f.write(str(args))
        # f.close()
        # time.sleep(10)
        return "success" 
    except:
        return "failed"

def make_celery(app):
    # celery = current_celery_app
    # celery.config_from_object(app.config, namespace="CELERY")
    celery = Celery(
        __name__,
        backend=CeleryConfig.RESULT_BACKEND,
        broker=CeleryConfig.BROKER_URL
    )
    celery.conf.update(app.config)
    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery




