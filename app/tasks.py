from celery import Celery
from app.util.utility import getPhonenumber
from config import CeleryConfig
from config import keyword_field, phone_field
from celery import shared_task, group
from bson import json_util
from app.functions.leadautomator import LeadAutomator
from app.functions.site_base import SiteAutomator
import json
from celery.utils.log import get_task_logger
from app.functions.finder import common_member


celery_logger = get_task_logger(__name__)
celery_app = Celery(__name__,
                    broker=CeleryConfig.BROKER_URL,
                    backend=CeleryConfig.RESULT_BACKEND
                    )


@celery_app.task(name="app.tasks.check")
def check_celery():
    print("celery working")


@celery_app.task()
def lead(**lead_data):
    try:
        celery_logger.info("lead automator started")
        lead_data["email"] = str(lead_data["email"]).lower()
        lead_data["phone"] = getPhonenumber([lead_data[field] for field in phone_field])
        if lead_data['phone'] is None:
            return "phonenumber not found"

        LA = LeadAutomator(lead_data=lead_data)
        LA.create_lead()
        for _ in keyword_field:
            LA.get_keywords(lead_data.get(_["field"], ""), ";")
        if len(LA.keywords) == 0:
            LA.get_keywords("None (default)", ";")
        site_list = LA.search_by_keyword()
        site_list = json.loads(json_util.dumps(site_list))
        task_list = []
        for _site in site_list:
            site_name = _site['name']
            site_projectname = _site['project_list']['project_name']
            try:
                if 'days' not in _site:
                    _site['days'] = 30
            except:
                _site['days'] = 30
            celery_logger.info(f"Site: {site_name}; Project: {site_projectname}")
            task_list.append(browserAutomate.s(_site, lead_data))
        job = group(task_list)
        output = job.apply_async(queue="browser")
        print(output)
        result = "success"
        celery_logger.info("task sent to browser queue")
        return result
    except Exception:
        celery_logger.exception("problem in sending lead")
        return "problem in sending lead"


@celery_app.task
def run_apis():
    try:
        celery_logger.info("API registration started")
        # import time
        # import schedule
        from app.util.utility import housing_api, magicbricks_api

        try:
            housing_api()
        except:
            pass
        try:
            magicbricks_api()
        except:
            pass
        
        # schedule.every(60).seconds.do(housing)
        # schedule.every(60).seconds.do(magicbricks)

        # while True:
        #     celery_logger.info("running APIs")
        #     schedule.run_pending()
        #     time.sleep(6)
    
    except Exception:
        celery_logger.exception("problem in running APIs")
        return "problem in running APIs"


@shared_task()
def browserAutomate(_site, lead_data):
    celery_logger.info("browser started")
    site_name = _site['name']
    site_projectname = _site['project_list']['project_name']
    ##
    site_keywords = []
    project_enquired = lead_data.get("project_enquired_for", "").split(";")
    interested_project = lead_data.get("interested_properties", "").split(";")
    interested_localities = lead_data.get("interested_localities", "").split(";")
    site_keywords.extend(project_enquired)
    site_keywords.extend(interested_project)
    site_keywords.extend(interested_localities)
    print(site_keywords)    
    ##
    match_keywords = common_member(site_keywords, _site['project_list']['keywords'])
    celery_logger.info(f"Site: {site_name}; Project: {site_projectname}")
    browserAutomation = SiteAutomator(  
                                    phone = lead_data["phone"],
                                    email= lead_data["email"],
                                    lead_data= lead_data,
                                    match_keywords= match_keywords,
                                    site_data=_site
                                        )
    browserAutomation.projectCheck(site_name, site_projectname)
    browserAutomation.automated_flow()
    # upload_result = browserAutomation.upload_data()
    # print(f"data upload :{upload_result}")
    browserAutomation.teardown()
    return "success"


@shared_task
def bulk_lead(*args):
    try:
        return "success"
    except Exception as e:
        print(str(e))
        return "failed"


def make_celery(app):
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
