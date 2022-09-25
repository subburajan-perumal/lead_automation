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


MONGO_DB = "REDACTED"

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
        },
        "removing_older_img": {
            "task": "app.tasks.removing_older_img",
            "schedule": crontab(hour='23')
        },
        "save_access_token": {
            "task": "app.tasks.save_access_token",
            "schedule": crontab(hour='*/10')
        }
}


@celery_app.task(name="app.tasks.check")
def check_celery():
    print("celery working")


@celery_app.task()
def lead(**lead_data):
    try:
        celery_logger.info("lead automator started")
        print("lead automator started")
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


@celery_app.task()
def bulk_lead(**lead_data):
    try:
        celery_logger.info("lead automator started")
        print("lead automator started")
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
        output = job.apply_async()
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
        from pymongo import MongoClient

        print('Housing')

        today = datetime.now()
        yesterday = today - timedelta(days = 1)
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

        CONN = MongoClient(MONGO_DB)
        DB = CONN['lead_automation']
        api_leads = DB['API_leads']

        for record in leads[::-1]:
            print(record)
            history = api_leads.find(
                {
                    'lead_phone': record['lead_phone'],
                    'latest_update': {
                        '$gte': datetime.now() - timedelta(days=1)
                    }
                }  
            )
            print(history)
            history = json.loads(json_util.dumps(history))
            print(history)
            
            if len(history) == 0:
                try:
                    logs.append(insert_record_to_zoho(record, type = 'housing'))
                    record['latest_update'] = datetime.now()
                    api_leads.update_one(
                        {
                            'lead_phone': record['lead_phone']
                        },
                        {
                            '$set': record
                        },
                        upsert = True
                    )
                except Exception as e:
                    logs.append(str(e))
                    record['latest_update'] = datetime.now()
                    api_leads.update_one(
                            {
                                'lead_phone': record['lead_phone']
                            },
                            {
                                '$set': record
                            },
                            upsert = True
                        )
                finally:
                    pass

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
        from pymongo import MongoClient

        print('Magicbricks')

        today = datetime.now()
        yesterday = today - timedelta(minutes=5)
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
        logs = []

        CONN = MongoClient(MONGO_DB)
        DB = CONN['lead_automation']
        api_leads = DB['API_leads']

        all_leads = leads['leadPojo']['leads']
        print(all_leads)

        if not all_leads:
            return {'status': 'Empty'}

        for input in all_leads:
            print(input)
            history = api_leads.find(
                {
                    'mobile': input['mobile'],
                    'latest_update': {
                        '$gte': datetime.now() - timedelta(days=1)
                    }
                }
            )
            print(history)
            history = json.loads(json_util.dumps(history))
            print(history)

            if len(history) == 0:
                try:
                    access_token = get_access_token()
                    project_id = getProjectID(input['project'], access_token)
                    print(input['project'], project_id)
                    if 'error' not in id:
                        access_token = get_access_token()
                        id = getProjectID('None (default)', access_token)
                    apartment_names = '2 BHK'
                    if '4 BHK' in input['msg']:
                        apartment_names = '4 BHK'
                    elif '3 BHK' in input['msg']:
                        apartment_names = '3 BHK'
                    if 'name' not in input:
                        input['name'] = 'Magicbricks User'
                    data = {
                        'Configuration1': apartment_names,
                        'Country_Code': '+' + str(input['isd']),
                        'City': input['city'],
                        'Email': input['email'],
                        'Phone': input['mobile'],
                        'Project_Enquired_for': dict({'id': project_id}),
                        'Full_Name': input['name'],
                        'Automation_Updates': str('Subject: ') + str(input['subject']) + str('\n\n') + str('Message: ') + str(input['msg']) + str('\n\n') + str(input),
                        'Lead_Source': 'Magicbricks automation'
                    }
                    if type(input['locality']) == str:
                        data['Interested_Localities'] = [input['locality']]
                    else:
                        data['Interested_Localities'] = list(input['locality'])                
                    print(data)
                    response = insert_records(data, access_token)
                    print(response)
                    logs.append(response)
                    input['latest_update'] = datetime.now()
                    api_leads.update_one(
                            {
                                'mobile': input['mobile']
                            },
                            {
                                '$set': input
                            },
                            upsert = True
                        )

                except Exception as e:
                    logs.append(str(e))
                    input['latest_update'] = datetime.now()
                    api_leads.update_one(
                            {
                                'mobile': input['mobile']
                            },
                            {
                                '$set': input
                            },
                            upsert = True
                        )
                finally:
                    pass        
        return logs
    
    except Exception as e:
        return {'error': str(e)}


@celery_app.task
def removing_older_img():
    import glob
    import os
    import time

    print('Remove older files running')

    path = r"storage/**/*.png"
    now = time.time()
    days = 200

    for filename in glob.iglob(path, recursive=True):
        if os.path.getmtime(os.path.join(path, filename)) < now - days * 86400:
            if os.path.isfile(os.path.join(path, filename)):
                print(filename)
                os.remove(os.path.join(path, filename))

    return {'status': 'Completed'}


@celery_app.task
def save_access_token():
    from requests.structures import CaseInsensitiveDict
    import os
    from requests import post

    print('Save access token running')

    zoho = {
        "URL": "https://www.zohoapis.com/crm/v2/Leads/",
        "CLIENT_ID": "REDACTED",
        "CLIENT_SECRET": "REDACTED",
        "REFRESH_TOKEN": "REDACTED",
        "REDIRECT_URI": "https://example.com",
        "NAME": "Zoho"
        }

    url = 'https://accounts.zoho.com/oauth/v2/token?client_id={}&client_secret={}&refresh_token={}&grant_type=refresh_token'.format(
            zoho['CLIENT_ID'],
            zoho['CLIENT_SECRET'],
            zoho['REFRESH_TOKEN'])

    headers = CaseInsensitiveDict()
    headers["Content-Length"] = "0"
    resp = post(url, headers=headers)
    output = resp.json()
    print(output)
    print("before :", os.environ.get("access-token"))
    access_token = output['access_token']
    os.environ["access_token"] = str(access_token)

    access_token = os.environ.get("access_token")
    print("after :", access_token)
  
    return access_token    


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


# @shared_task
# def bulk_lead(*args):
#     try:
#         return "success"
#     except Exception as e:
#         print(str(e))
#         return "failed"


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
