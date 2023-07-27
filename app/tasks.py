import glob
import json
import os
import time
from datetime import datetime, timedelta

import pytz
import requests
import xmltodict
from bson import json_util
from celery import Celery, group, shared_task
from celery.schedules import crontab
from celery.signals import worker_init
from celery.utils.log import get_task_logger

from app.database import get_db
from app.functions.finder import common_member
from app.functions.leadautomator import LeadAutomator
from app.util.utility import getPhonenumber, getProjectID, insert_records, refresh_access_token
from config import CeleryConfig, Config, keyword_field, phone_field


celery_logger = get_task_logger(__name__)
celery_app = Celery(__name__,
                    broker=CeleryConfig.BROKER_URL,
                    backend=CeleryConfig.RESULT_BACKEND
                    )

celery_app.conf.task_default_queue = 'default'

celery_app.conf.task_routes = {
    'app.tasks.run_magicbricks_api': {'queue': 'api_lead'},
    'app.tasks.run_99acres_api': {'queue': 'api_lead'},
    'app.tasks.bulk_lead': {'queue': 'bulk'},
    'app.tasks.lead': {'queue': 'lead'},
    'app.tasks.removing_older_img': {'queue': 'lead'},
    'app.tasks.save_access_token': {'queue': 'lead'},
    'app.tasks.browserAutomate': {'queue': 'browser'},
    }

celery_app.conf.beat_schedule = {
        "run_magicbricks_api": {
            "task": "app.tasks.run_magicbricks_api",
            "schedule": crontab(minute=0)
        },
        "run_99acres_api": {
            "task": "app.tasks.run_99acres_api",
            "schedule": crontab(minute=0)
        },
        "removing_older_img": {
            "task": "app.tasks.removing_older_img",
            "schedule": crontab(minute=0, hour=23)
        },
        "save_access_token": {
            "task": "app.tasks.save_access_token",
            "schedule": crontab(minute='*/30')
        }
}

IST = pytz.timezone('Asia/Kolkata')
SCREENSHOT_RETENTION_DAYS = 200


@worker_init.connect
def check_settings(**_):
    Config.validate()


@celery_app.task(name="app.tasks.check")
def check_celery():
    celery_logger.info("celery working")


def _dispatch_to_sites(lead_data, automate_task, queue):
    """Create the lead, match it to site projects by keyword, and fan out one browser task per project."""
    automator = LeadAutomator(lead_data=lead_data)
    automator.create_lead()
    for field in keyword_field:
        automator.get_keywords(lead_data.get(field["field"]) or "", field["seperator"])
    if len(automator.keywords) == 0:
        automator.get_keywords("None (default)", ";")
    site_list = json.loads(json_util.dumps(automator.search_by_keyword()))

    task_list = []
    for _site in site_list:
        _site.setdefault('days', 30)
        celery_logger.info(f"Site: {_site['name']}; Project: {_site['project_list']['project_name']}")
        task_list.append(automate_task.s(_site, lead_data))
    if task_list:
        group(task_list).apply_async(queue=queue)
    return len(task_list)


@celery_app.task()
def lead(**lead_data):
    try:
        celery_logger.info("lead automator started")
        lead_data["email"] = str(lead_data.get("email", "")).lower()
        lead_data["phone"] = getPhonenumber([lead_data.get(field) for field in phone_field])
        if lead_data['phone'] is None:
            return "phonenumber not found"
        lead_data.setdefault("source", "zoho")

        sent = _dispatch_to_sites(lead_data, browserAutomate, "browser")
        celery_logger.info("%s task(s) sent to browser queue", sent)
        return "success"
    except Exception:
        celery_logger.exception("problem in sending lead")
        return "problem in sending lead"


@celery_app.task()
def bulk_lead(**lead_data):
    try:
        celery_logger.info("bulk lead automator started")
        lead_data["email"] = str(lead_data.get("email", "")).lower()
        lead_data["phone"] = getPhonenumber([lead_data.get('phone')])
        if lead_data['phone'] is None:
            return {"msg": "phonenumber not found"}
        lead_data.setdefault("source", "bulk_upload")

        sent = _dispatch_to_sites(lead_data, browserAutomateBulk, "bulk")
        celery_logger.info("%s task(s) sent to bulk queue", sent)
        return {"result": "success"}
    except Exception:
        celery_logger.exception("problem in sending lead")
        return {"msg": "problem in sending lead"}


def _project_id_or_default(project_name):
    project_id = getProjectID(project_name)
    if isinstance(project_id, dict):
        project_id = getProjectID('None')
    return project_id


def _recently_synced(api_leads, phone_key, phone):
    return api_leads.find_one(
        {
            phone_key: phone,
            'latest_update': {'$gte': datetime.now() - timedelta(days=1)}
        }
    ) is not None


# MAGICBRICKS AUTOMATION

@celery_app.task
def run_magicbricks_api():
    if not Config.MAGICBRICKS_API_KEY:
        return {'error': 'MAGICBRICKS_API_KEY is not set'}
    try:
        now = datetime.now(IST)
        params = {
            'key': Config.MAGICBRICKS_API_KEY,
            'startDate': (now - timedelta(days=2)).strftime('%Y%m%d'),
            'endDate': (now + timedelta(days=2)).strftime('%Y%m%d'),
        }
        resp = requests.get('http://rating.magicbricks.com/mbRating/download.json', params=params, timeout=60)
        resp.raise_for_status()
        all_leads = (resp.json().get('leadPojo') or {}).get('leads') or []
        if len(all_leads) == 0:
            return {'status': 'Empty'}

        api_leads = get_db()['API_leads']
        logs = []
        for input in all_leads:
            if _recently_synced(api_leads, 'mobile', input.get('mobile')):
                continue
            try:
                msg = str(input.get('msg') or '')
                apartment_names = '2 BHK'
                if '4 BHK' in msg:
                    apartment_names = '4 BHK'
                elif '3 BHK' in msg:
                    apartment_names = '3 BHK'
                if not input.get('name'):
                    input['name'] = 'Magicbricks User'
                if not input.get('email'):
                    input['email'] = str(input['mobile']) + '@example.com'
                details = (msg + '\n\n' + str(input))[:200]
                data = {
                    'Configuration1': apartment_names,
                    'Country_Code': '+' + str(input.get('isd') or '91'),
                    'City': input.get('city'),
                    'Email': input['email'],
                    'Phone': input['mobile'],
                    'Project_Enquired_for': {'id': _project_id_or_default(input.get('project'))},
                    'Full_Name': input['name'],
                    'Lead_Source': 'Magicbricks',
                    'Last_Name': input['name'],
                    'Initial_Enquiry_Particulars_Automation': details
                }
                locality = input.get('locality')
                if not locality:
                    data['Interested_Localities'] = None
                elif isinstance(locality, str):
                    data['Interested_Localities'] = [locality]
                else:
                    data['Interested_Localities'] = list(locality)

                response = insert_records(data)
                logs.append(response)
                input['latest_update'] = datetime.now()
                input['response'] = response
                api_leads.update_one({'mobile': input['mobile']}, {'$set': input}, upsert=True)

            except Exception as e:
                celery_logger.exception("Magicbricks lead failed")
                logs.append(str(e))

        return logs

    except Exception as e:
        celery_logger.exception("Magicbricks sync failed")
        return {'error': str(e)}


# 99ACRES AUTOMATION

def _format_99acres_lead(lead):
    contact = lead.get('CntctDtl') or {}
    query = lead.get('QryDtl') or {}
    phone = contact.get('Phone')
    info = query.get('QryInfo')
    try:
        country_code = str(phone).split('-')[0][1:] or '91'
    except Exception:
        country_code = '91'
    return {
        'Full_Name': contact.get('Name') or '99acres User',
        'Email': contact.get('Email') or str(phone) + '@example.com',
        'Phone': phone,
        'Project_Enquired_for': query.get('ProjName'),
        'Automation Updates': 'Subject: ' + str(info)[:200] if info else 'NIL',
        'Country_Code': country_code,
    }


@celery_app.task
def run_99acres_api():
    if not (Config.ACRES99_USERNAME and Config.ACRES99_PASSWORD and Config.ACRES99_API_TOKEN):
        return {'error': '99acres credentials are not set'}
    try:
        now = datetime.now(IST)
        # FORMAT: 2022-11-29 23:59:59
        today = now.strftime("%Y-%m-%d %H:%M:%S")
        yesterday = (now - timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")

        url = "https://www.99acres.com/99api/v1/getmy99Response/{}/uid/".format(Config.ACRES99_API_TOKEN)
        query = xmltodict.unparse({'query': {
            'user_name': Config.ACRES99_USERNAME,
            'pswd': Config.ACRES99_PASSWORD,
            'start_date': yesterday,
            'end_date': today,
        }}, full_document=False)
        payload = {'xml': "<?xml version='1.0'?>" + query}
        response = requests.post(url, data=payload, timeout=60)
        response.raise_for_status()
        resp = (xmltodict.parse(response.content).get('Xml') or {}).get('Resp') or []
        # xmltodict returns a dict, not a list, when there is exactly one lead.
        if isinstance(resp, dict):
            resp = [resp]

        formatted_leads = []
        for lead in resp:
            try:
                formatted_leads.append(_format_99acres_lead(lead))
            except Exception:
                celery_logger.exception("could not read a 99acres lead")

        if len(formatted_leads) == 0:
            return {'status': 'Empty'}

        api_leads = get_db()['API_leads']
        logs = []
        for input in formatted_leads:
            if not input['Phone'] or _recently_synced(api_leads, 'Phone', input['Phone']):
                continue
            try:
                data = {
                    'Configuration1': '2 BHK',
                    'Country_Code': '+' + str(input['Country_Code']),
                    'Email': input['Email'],
                    'Phone': input['Phone'],
                    'Project_Enquired_for': {'id': _project_id_or_default(input['Project_Enquired_for'])},
                    'Full_Name': input['Full_Name'],
                    'Lead_Source': '99acres',
                    'Last_Name': input['Full_Name'],
                    'Initial_Enquiry_Particulars_Automation': input['Automation Updates']
                }

                response = insert_records(data)
                logs.append(response)
                input['latest_update'] = datetime.now()
                input['details'] = data
                input['response'] = response
                api_leads.update_one({'Phone': input['Phone']}, {'$set': input}, upsert=True)

            except Exception as e:
                celery_logger.exception("99acres lead failed")
                logs.append(str(e))

        return logs

    except Exception as e:
        celery_logger.exception("99acres sync failed")
        return {'error': str(e)}


@celery_app.task
def removing_older_img():
    cutoff = time.time() - SCREENSHOT_RETENTION_DAYS * 86400
    removed = 0
    for filename in glob.iglob(os.path.join(Config.STORAGE_PATH, "**", "*.png"), recursive=True):
        try:
            if os.path.isfile(filename) and os.path.getmtime(filename) < cutoff:
                os.remove(filename)
                removed += 1
        except OSError:
            celery_logger.exception("could not remove %s", filename)
    celery_logger.info("removed %s screenshots older than %s days", removed, SCREENSHOT_RETENTION_DAYS)
    return {'status': 'Completed', 'removed': removed}


@celery_app.task
def save_access_token():
    """Keep a fresh Zoho access token cached in Redis so lead tasks never wait on a refresh."""
    refresh_access_token()
    celery_logger.info("Zoho access token refreshed")
    return "refreshed"


def _run_site_automation(automator_class, _site, lead_data):
    match_keywords = common_member(_lead_keywords(lead_data), _site['project_list']['keywords'])
    if match_keywords is None:
        return "No matched keywords found"
    site_name = _site['name']
    site_projectname = _site['project_list']['project_name']
    celery_logger.info(f"Site: {site_name}; Project: {site_projectname}; matched: {match_keywords}")
    browserAutomation = automator_class(
                                    phone=lead_data["phone"],
                                    email=lead_data["email"],
                                    lead_data=lead_data,
                                    match_keywords=match_keywords,
                                    site_data=_site
                                    )
    try:
        browserAutomation.projectCheck(site_name, site_projectname)
        browserAutomation.automated_flow()
    finally:
        # Always close Firefox, or a failed site leaves a browser process behind on the worker.
        browserAutomation.teardown()
    return "success"


def _lead_keywords(lead_data):
    keywords = []
    for field in ("project_enquired_for", "interested_properties", "interested_localities"):
        keywords.extend((lead_data.get(field) or "").split(";"))
    return keywords


@shared_task()
def browserAutomate(_site, lead_data):
    from app.functions.site_base import SiteAutomator
    return _run_site_automation(SiteAutomator, _site, lead_data)


@shared_task()
def browserAutomateBulk(_site, lead_data):
    from app.functions.site_automator_bulk import SiteAutomator
    return _run_site_automation(SiteAutomator, _site, lead_data)

