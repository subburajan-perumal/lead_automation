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
from celery.schedules import crontab


celery_logger = get_task_logger(__name__)
celery_app = Celery(__name__,
                    broker=CeleryConfig.BROKER_URL,
                    backend=CeleryConfig.RESULT_BACKEND
                    )

celery_app.conf.beat_schedule = {
        "run_housing_api": {
            "task": "app.tasks.run_housing_api",
            "schedule": crontab(hour='*/1')
        },
        "run_magicbricks_api": {
            "task": "app.tasks.run_magicbricks_api",
            "schedule": crontab(hour='*/1')
        }        
}


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
def run_housing_api():
    try:
        import requests
        import hmac
        import hashlib
        from datetime import datetime, timedelta
        import time
        import pytz
        from app.util.utility import insert_record_to_zoho

        celery_logger.info('Housing')

        today = datetime.now()
        yesterday = today - timedelta(minutes = 10)
        today = today.astimezone(pytz.timezone('Asia/Kolkata'))
        yesterday = yesterday.astimezone(pytz.timezone('Asia/Kolkata'))

        yesterday = int(time.mktime(yesterday.timetuple()))
        today = int(time.mktime(today.timetuple()))
        timestamp = today

        id = 2674965
        key = "REDACTED"
        timestamp = str(timestamp)
        byte_key = bytes(key, 'UTF-8')
        message = timestamp.encode()
        hash = hmac.new(byte_key, message, hashlib.sha256).hexdigest()
        params = {
            'start_date': str(yesterday),
            'end_date': str(today),
            'current_time': str(timestamp),
            'hash': str(hash),
            'id': id
        }
        url = 'https://leads.housing.com/api/v0/get-builder-leads'
        resp = requests.get(url = url, params = params)
        leads = resp.json()
        print(leads)
        logs = []

        for record in leads[::-1]:
            try:
                logs.append(insert_record_to_zoho(record, type = 'housing'))
            except Exception as e:
                logs.append(str(e))
        return logs

    except Exception as e:
        return {'error': str(e)}


@celery_app.task
def run_magicbricks_api():
    try:
        import requests
        from datetime import datetime, timedelta
        import pytz
        from json import loads
        from app.util.utility import insert_records, get_access_token, getProjectID

        print('Magicbricks')

        today = datetime.now()
        yesterday = today - timedelta(minutes=20)
        today = today.astimezone(pytz.timezone('Asia/Kolkata'))
        yesterday = yesterday.astimezone(pytz.timezone('Asia/Kolkata'))

        yesterday = datetime.strptime(str(yesterday).split(' ')[0], '%Y-%m-%d').strftime('%Y%m%d')
        today = datetime.strptime(str(today).split(' ')[0], '%Y-%m-%d').strftime('%Y%m%d')
        
        key = 'REDACTED_MAGICBRICKS_KEY'
        params = {
            'key': key,
            'endDate': today,
            'startDate': yesterday,
        }
        url = 'http://rating.magicbricks.com/mbRating/download.json'
        resp = requests.get(url = url, params = params)
        leads = loads(resp.content)
        print(leads)
        logs = []

        for input in leads['leadPojo']['leads']:
            try:
                access_token = get_access_token()
                project_id = getProjectID(input['project'], access_token)
                print(input['project'], project_id)
                if 'error' not in project_id:
                    apartment_names = []
                    if '2 BHK' in input['msg']:
                        apartment_names.append('2 BHK')
                    if '3 BHK' in input['msg']:
                        apartment_names.append('3 BHK')
                    if '4 BHK' in input['msg']:
                        apartment_names.append('4 BHK')
                    print(list(apartment_names))
                    data = {
                        'Configuration1': list(apartment_names),
                        'Country_Code': '+' + str(input['isd']),
                        # 'Interested_Localities': input['locality'],
                        'City': input['city'],
                        'Email': input['email'],
                        'Phone': input['mobile'],
                        'Project_Enquired_for': dict({'id': project_id}),
                        'Full_Name': input['name'],
                        'Automation Updates': str('Subject: ') + str(input['subject']) + str('\n\n') + str('Message: ') + str(input['msg']) + str('\n\n') + str(input),
                        'Lead_Source': 'magicbricks_automation'
                    }
                    if type(input['locality']) == str:
                        data['Interested_Localities'] = [input['locality']]
                    else:
                        data['Interested_Localities'] = list(input['locality'])                
                    print(data)
                    response = insert_records(data, access_token)
                    print(response)
                    logs.append(response)
            except Exception as e:
                logs.append(str(e))
        
        return logs
    
    except Exception as e:
        return {'error': str(e)}


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
