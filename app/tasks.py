from asyncio.log import logger
from celery import Celery
from app.util.utility import getPhonenumber
from config import CeleryConfig
from config import keyword_field, phone_field
from celery import shared_task, group
from bson import json_util
from app.functions.leadautomator import LeadAutomator
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

celery_app.conf.task_default_queue = 'default'

celery_app.conf.task_routes = {
    'app.tasks.run_housing_api': {'queue': 'lead'},
    'app.tasks.run_magicbricks_api': {'queue': 'lead'},
    'app.tasks.run_99acres_api': {'queue': 'lead'},
    'app.tasks.bulk_lead': {'queue': 'bulk'},
    'app.tasks.lead': {'queue': 'lead'},
    'app.tasks.removing_older_img': {'queue': 'lead'},
    'app.tasks.save_access_token': {'queue': 'lead'},
    'app.tasks.browserAutomate': {'queue': 'browser'},
    }

celery_app.conf.beat_schedule = {
        "run_housing_api": {
            "task": "app.tasks.run_housing_api",
            "schedule": crontab(hour='*/1')
        },
        "run_magicbricks_api": {
            "task": "app.tasks.run_magicbricks_api",
            "schedule": crontab(hour='*/1')
        },
        "run_99acres_api": {
            "task": "app.tasks.run_99acres_api",
            "schedule": crontab(hour='*/1')
        },
        "removing_older_img": {
            "task": "app.tasks.removing_older_img",
            "schedule": crontab(hour='23')
        },
        "save_access_token": {
            "task": "app.tasks.save_access_token",
            "schedule": crontab(minute='*/30')
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
        print("site_list in task.py")
        print(site_list)
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
async def bulk_lead(**lead_data):
    try:
        celery_logger.info("bulk lead automator started")
        print("bulk lead automator started")
        print(lead_data)
        lead_data["email"] = str(lead_data["email"]).lower()
        if getPhonenumber([lead_data['phone']]):
            lead_data["phone"] = getPhonenumber([lead_data['phone']])
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
        print('site_list: ', site_list)
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
            task_list.append(browserAutomateBulk.s(_site, lead_data))
        print('task_list: ', task_list)
        job = group(task_list)
        output = job.apply_async(queue='bulk')
        print(output)
        result = "success"
        celery_logger.info("task sent to browser queue")
        return result
    except Exception:
        celery_logger.exception("problem in sending lead")
        return "problem in sending lead"

# HOUSING AUTOMATION

@celery_app.task
def run_housing_api():
    try:
        import requests
        import hmac
        import hashlib
        from datetime import datetime, timedelta
        import time
        import pytz
        from app.util.utility import insert_records, get_access_token, getProjectID
        from pymongo import MongoClient

        print('Housing')

        today = datetime.now() + timedelta(days=1)
        yesterday = today - timedelta(days = 2)
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
        logs = []

        CONN = MongoClient(MONGO_DB)
        DB = CONN['lead_automation']
        api_leads = DB['API_leads']

        for record in leads[::-1]:
            history = api_leads.find(
                {
                    'lead_phone': record['lead_phone'],
                    'latest_update': {
                        '$gte': datetime.now() - timedelta(days=1)
                    }
                }  
            )
            history = json.loads(json_util.dumps(history))
            # print(history)
            
            if len(history) == 0:
                print(record)
                try:
                    access_token = get_access_token()
                    project_id = getProjectID(record['project_name'], access_token)
                    print((record['project_name'], project_id))
                    
                    if 'error' in project_id:
                        access_token = get_access_token()
                        project_id = getProjectID('None', access_token)

                    if 'lead_email' not in record or record['lead_email'] == None:
                        record['lead_email'] = record['lead_phone'] + '@example.com'
                    if 'lead_name' not in record or record['lead_name'] == None:
                        record['lead_name'] = 'Housing User'
                    apartment_names = '2 BHK'
                    if '4 BHK' in str(record['apartment_names']):
                        apartment_names = '4 BHK'
                    elif '3 BHK' in str(record['apartment_names']):
                        apartment_names = '3 BHK'

                    data = {
                        'Configuration1': apartment_names,
                        'Country_Code': str(record['country_code']),
                        'City': record['city_name'],
                        'Email': record['lead_email'],
                        'Phone': record['lead_phone'],
                        'Project_Enquired_for': dict(
                            {'id': project_id}
                        ),
                        'Full_Name': record['lead_name'],
                        'Last_Name': record['lead_name'],
                        'Lead_Source': 'Housing',
                        'Initial_Enquiry_Particulars_Automation': str(record)[:200]
                    }

                    if not record['locality_name']:
                        data['Interested_Localities'] = None
                    elif type(record['locality_name']) == str:
                        data['Interested_Localities'] = [record['locality_name']]
                    else:
                        data['Interested_Localities'] = list(record['locality_name'])

                    if record['service_type'] == 'new-projects':
                        data['Interested_in_wf'] = 'New'                    
                    
                    print(('data', data))
                    response = insert_records(data, access_token)
                    print(('response', response))
                    logs.append(response)
                    record['latest_update'] = datetime.now()
                    record['response'] = response
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

        return logs

    except Exception as e:
        return {'error': str(e)}


# MAGICBRICKS AUTOMATION

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

        today = datetime.now() + timedelta(days=2)
        yesterday = today - timedelta(days=4)
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

        if len(all_leads) == 0:
            return {'status': 'Empty'}

        for input in all_leads:
            # print(input)
            history = api_leads.find(
                {
                    'mobile': input['mobile'],
                    'latest_update': {
                        '$gte': datetime.now() - timedelta(days=1)
                    }
                }
            )
            history = json.loads(json_util.dumps(history))
            # print(history)

            if len(history) == 0:
                print(input)
                try:
                    access_token = get_access_token()
                    project_id = getProjectID(input['project'], access_token)
                    print((input['project'], project_id))
                    if 'error' in project_id:
                        access_token = get_access_token()
                        project_id = getProjectID('None', access_token)
                    apartment_names = '2 BHK'
                    if '4 BHK' in input['msg']:
                        apartment_names = '4 BHK'
                    elif '3 BHK' in input['msg']:
                        apartment_names = '3 BHK'
                    if 'name' not in input or input['name'] == None:
                        input['name'] = 'Magicbricks User'
                    if 'email' not in input or input['email'] == None:
                        input['email'] = str(input['mobile']) + '@example.com'
                    details = str(input['msg']) + str('\n\n') + str(input)
                    details = details[:200]
                    data = {
                        'Configuration1': apartment_names,
                        'Country_Code': '+' + str(input['isd']),
                        'City': input['city'],
                        'Email': input['email'],
                        'Phone': input['mobile'],
                        'Project_Enquired_for': dict({'id': project_id}),
                        'Full_Name': input['name'],
                        'Lead_Source': 'Magicbricks',
                        'Last_Name': input['name'],
                        'Initial_Enquiry_Particulars_Automation': details
                    }
                    print(('data 1', data))
                    if not input['locality']:
                        data['Interested_Localities'] = None
                    elif type(input['locality']) == str:
                        data['Interested_Localities'] = [input['locality']]
                    else:
                        data['Interested_Localities'] = list(input['locality'])                
                    print(data)
                    response = insert_records(data, access_token)
                    print(response)
                    logs.append(response)
                    input['latest_update'] = datetime.now()
                    input['response'] = response
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

        return logs
    
    except Exception as e:
        return {'error': str(e)}



# 99ACRES AUTOMATION

@celery_app.task
def run_99acres_api():
    try:
        import requests
        from datetime import datetime, timedelta
        import pytz
        import xmltodict
        from bson import json_util
        from app.util.utility import insert_records, get_access_token, getProjectID
        from pymongo import MongoClient

        print('99acres')

        today = datetime.now()
        yesterday = today - timedelta(days=1)
        today = today.astimezone(pytz.timezone('Asia/Kolkata'))
        yesterday = yesterday.astimezone(pytz.timezone('Asia/Kolkata'))
        today = datetime.strptime(str(today).split('.')[0], "%Y-%m-%d %H:%M:%S")
        yesterday = datetime.strptime(str(yesterday).split('.')[0], "%Y-%m-%d %H:%M:%S")

        # FORMAT: 2022-11-29 23:59:59

        username = 'REDACTED_99ACRES_USER'
        password = 'REDACTED'
        url = "https://www.99acres.com/99api/v1/getmy99Response/REDACTED_99ACRES_TOKEN/uid/"

        payload={'xml': '<?xml version=\\\'1.0\\\'?><query><user_name>{}</user_name><pswd>{}</pswd><start_date>{}</start_date><end_date>{}</end_date></query>'.format(username, password, yesterday, today)}
        files=[]
        headers = {}
        response = requests.request("POST", url, headers=headers, data=payload, files=files)
        data_dict = xmltodict.parse(response.content)
        all_leads = data_dict['Xml']['Resp']
        formatted_leads = []

        for lead in all_leads:
            try:
                data = dict()
                if 'Name' not in lead['CntctDtl'] or lead['CntctDtl'] == None:
                    data['Full_Name'] = '99acres User'
                else:
                    data['Full_Name'] = lead['CntctDtl']['Name']
                if 'Email' not in lead['CntctDtl'] or lead['CntctDtl'] == None:
                    data['Email'] = str(lead['CntctDtl']['Phone']) + '@example.com'
                else:
                    data['Email'] = lead['CntctDtl']['Email']
                if 'Phone' not in lead['CntctDtl'] or lead['CntctDtl'] == None:
                    data['Phone'] = None
                else:
                    data['Phone'] = lead['CntctDtl']['Phone']                    
                try:
                    data['Project_Enquired_for'] = lead['QryDtl']['ProjName']
                except:
                    data['Project_Enquired_for'] = None
                if 'QryInfo' not in lead['QryDtl']:
                    data['Automation Updates'] = 'NIL'
                else:
                    data['Automation Updates'] = str('Subject: ') + lead['QryDtl']['QryInfo'][:200]
                try:
                    data['Country_Code'] = str(lead['CntctDtl']['Phone']).split('-')[0][1:]
                except:
                    data['Country_Code'] = '91'
            
                formatted_leads.append(data)
            
            except:
                pass        

        print(formatted_leads)
        CONN = MongoClient(MONGO_DB)
        DB = CONN['lead_automation']
        api_leads = DB['API_leads']
        logs = []

        if len(formatted_leads) == 0:
            return {'status': 'Empty'}

        for input in formatted_leads:
            history = api_leads.find(
                {
                    'Phone': input['Phone'],
                    'latest_update': {
                        '$gte': datetime.now() - timedelta(days=1)
                    }
                }
            )
            history = json.loads(json_util.dumps(history))

            if len(history) == 0:
                print('input: ', input)
                try:
                    access_token = get_access_token()
                    project_id = getProjectID(input['Project_Enquired_for'], access_token)
                    print((input['Project_Enquired_for'], project_id))
                    if 'error' in project_id:
                        access_token = get_access_token()
                        project_id = getProjectID('None', access_token)

                    data = {
                        'Configuration1': '2 BHK',
                        'Country_Code': '+' + str(input['Country_Code']),
                        'Email': input['Email'],
                        'Phone': input['Phone'],
                        'Project_Enquired_for': dict({'id': project_id}),
                        'Full_Name': input['Full_Name'],
                        'Lead_Source': '99acres',
                        'Last_Name': input['Full_Name'],
                        'Initial_Enquiry_Particulars_Automation': input['Automation Updates']
                    }                    
                    
                    response = insert_records(data, access_token)
                    logs.append(response)
                    input['latest_update'] = datetime.now()
                    input['details'] = data
                    input['response'] = response
                    api_leads.update_one(
                            {
                                'Phone': input['Phone']
                            },
                            {
                                '$set': input
                            },
                            upsert = True
                        )

                except Exception as e:
                    logs.append(str(e))

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
                try:
                    os.remove(os.path.join(path, filename))
                except:
                    pass
    
    return {'status': 'Completed'}


@celery_app.task
def save_access_token():
    from requests.structures import CaseInsensitiveDict
    import os
    from requests import post
    from dotenv import load_dotenv, set_key, find_dotenv, get_key

    print('Save access token running')

    zoho = {
        "URL": "https://www.zohoapis.com/crm/v2/Leads/",
        "CLIENT_ID": "REDACTED",
        "CLIENT_SECRET": "REDACTED",
        # "REFRESH_TOKEN": "REDACTED",
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
    dotenv_file = find_dotenv()
    load_dotenv(dotenv_file)
    # print("before :", os.environ.get("access_token"))
    # print('before: {}'.format(os.getenv('access_token')))
    before = get_key(dotenv_file, 'access_token', encoding='utf-8')
    print('before: {}'.format(before))
    access_token = output['access_token']
    # os.environ["access_token"] = str(access_token)
    set_key(dotenv_file, "access_token", access_token)
    # access_token = os.environ.get("access_token")
    # access_token = os.getenv('access_token')
    access_token = get_key(dotenv_file, 'access_token', encoding='utf-8')
    print("after :", access_token)
  
    return access_token


@shared_task()
def browserAutomate(_site, lead_data):
    from app.functions.site_base import SiteAutomator

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
    logger.info("site_keywords in tasks.py")
    logger.info(site_keywords) 
    print("site_keywords in tasks.py")
    print(site_keywords)    
    logger.info("project keywords in tasks.py")
    logger.info(_site['project_list']['keywords']) 
    print("project keywords in tasks.py")
    print(_site['project_list']['keywords']) 
    ##
    match_keywords = common_member(site_keywords, _site['project_list']['keywords'])
    print("match keywords in tasks.py")
    print(match_keywords)
    if match_keywords == None:
        return "No matched keywords found"
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


@shared_task()
async def browserAutomateBulk(_site, lead_data):
    from app.functions.site_automator_bulk import SiteAutomator

    celery_logger.info("browser started")
    site_name = _site['name']
    site_projectname = _site['project_list']['project_name']
    site_keywords = []
    project_enquired = lead_data.get("project_enquired_for", "").split(";")
    interested_project = lead_data.get("interested_properties", "").split(";")
    interested_localities = lead_data.get("interested_localities", "").split(";")
    site_keywords.extend(project_enquired)
    site_keywords.extend(interested_project)
    site_keywords.extend(interested_localities)
    print(site_keywords)    
    match_keywords = common_member(site_keywords, _site['project_list']['keywords'])
    if match_keywords == None:
        return "No matched keywords found"
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
