from celery import Celery
from numpy import maximum
from config import CeleryConfig
from config import keyword_field
from celery import shared_task, group
from bson import json_util
from app.functions.leadautomator import LeadAutomator
from app.functions.site_base import SiteAutomator
import json
from celery.utils.log import get_task_logger


logger = get_task_logger("task_logger")
celery_app = Celery(__name__,
                    broker=CeleryConfig.BROKER_URL,
                    backend=CeleryConfig.RESULT_BACKEND)


@celery_app.task(name="app.tasks.check")
def check_celery():
    print("celery working")


@celery_app.task(bind=True,max_retries=3)
def lead(self,**lead_data):
    try:
        logger.info("lead automator started")
        LA = LeadAutomator(lead_data=lead_data)
        LA.create_lead()
        for _ in keyword_field:
            LA.get_keywords(lead_data.get(_["field"], ""), ";")
        LA.get_keywords("None (default)", ";")
        site_list = LA.search_by_keyword()
        site_list = json.loads(json_util.dumps(site_list))
        task_list = []
        for _site in site_list:
            site_name = _site['name']
            site_projectname = _site['project_list']['project_name']
            logger.info(f"Site: {site_name}; Project: {site_projectname}")

            task_list.append(browserAutomate.s(_site, lead_data))
        job = group(task_list)
        output = job.apply_async(queue="browser")
        print(output)
        result = "success"
        logger.info("task sent to browser queue")
        return result
    except Exception as e:
        print(str(e))
        return "failed"


@shared_task(bind=True,max_retries=5)
def browserAutomate(self,_site, lead_data):
    logger.info("browser started")
    site_name = _site['name']
    site_projectname = _site['project_list']['project_name']
    logger.info(f"Site: {site_name}; Project: {site_projectname}")
    browserAutomation = SiteAutomator(
                                    lead_data["phone"],
                                    lead_data["email"],
                                    lead_data,
                                    site_data=_site)
    browserAutomation.projectCheck(site_name, site_projectname)
    browserAutomation.automated_flow()
    upload_result = browserAutomation.upload_data()
    print(f"data upload :{upload_result}")
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
