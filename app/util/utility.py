from json import dumps, loads
from datetime import datetime
import json
from urllib import response
from uuid import uuid4
import pytz
from requests import get, post
import pymongo
from bson import json_util
from celery.utils.log import get_task_logger

celery_logger = get_task_logger(__name__)


def cmpstring(string1, string2):
    str1 = "".join([i for i in string1 if i.isalpha()])
    str2 = "".join([i for i in string2 if i.isalpha()])
    return str1 == str2


def getTime():
    IST=pytz.timezone('Asia/Kolkata')
    now = datetime.now(IST)
    # print("now =", now)
    # dd/mm/YY H:M:S
    # dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    return now


def getPhonenumber(numberlist: list):
    import phonenumbers as PN
    # default_number=os.environ.get("")
    filter_number = []

    # numberstring = "".join(str(i) for i in numberlist)
    numbertext = PN.PhoneNumberMatcher(str(numberlist), None)
    # print(numbertext.has_next())

    for number in numbertext:
        print(filter_number.append(number.raw_string))

    for number in numberlist:
        if len(number) == 10:
            filter_number.append("+91"+number)
            print("filtered_array : ", filter_number)
    if len(filter_number) > 0:
        
        return(filter_number[0])
    else:
        return None


def getName(name):
    splited_name = name.split(" ")

    if len(splited_name) == 1:

        return splited_name[0], splited_name[0]
    elif len(splited_name) == 2:
        return splited_name[0], splited_name[1]
    elif len(splited_name) == 3:
        return splited_name[0]+splited_name[1], splited_name[2]
    else:
        return "" ""

# pre_akshaya_Adityaram_phase_5_krishnamoorthy perumal.png
# (site,sub_projectname,path,leadname)


def getsavePath(path, path2, site_name, sub_project_name, leadname):
    from config import Config
    MONGO_DB = Config.MONGO_URI
    try:
        # Connecting to Lead Automation MongoDB server to get filename(subname)
        CONN = pymongo.MongoClient(MONGO_DB)
        DB = CONN['lead_automation']
        SITE = DB['Site']

        result = SITE.find({"project_list.project_name": sub_project_name})
        result = json.loads(json_util.dumps(result))

        for elem in result[0]["project_list"]:
            if elem["project_name"] == sub_project_name:
                subname = elem["filename"]    
    except:
        subname = sub_project_name

    return [
        str(str(path) + '/' + "pre" + "_" + site_name + "_" + str(sub_project_name) +"_"+str(leadname).replace(" ", '_') + ".png"),
        str(str(path) + '/' + "post" + "_" + site_name + "_" + str(sub_project_name) +"_"+str(leadname).replace(" ", "_") + ".png"),
        str(str(path) + '/' + "err" + "_" + site_name + "_" + str(sub_project_name) +"_"+str(leadname).replace(" ", "_") + ".png"),
        str(str(path2) + '/' + "pre" + "_" + str(subname) + "_" + str(uuid4().hex) + ".png"),
        str(str(path2) + '/' + "post" + "_" + str(subname) + "_" + str(uuid4().hex) + ".png"),
        str(str(path2) + '/' + "err" + "_" + str(subname) + "_" + str(uuid4().hex) + ".png")
        ]
# print(getsavePath("akshaya","Tango"))+str(leadname).replace(" ","_")


# LeadAutomation Mapping

def mapping(input, id, type = 'lead_automation'):
    data = {
        'Configuration1': str(input['apartment_names']),
        'Country_Code': input['country_code'],
        'Zoning': input['category_type'],
        'City': input['city_name'],
        'Email': input['lead_email'],
        'Phone': input['lead_phone'],
        'Project_Enquired_for': dict(
            {'id': id}
        ),
        # 'Project_Enquired_for': '$' + input['project_name'],
        'Property_Type1': input['property_field'],
        'Minimum_Price': input['min_price'],
        'Maximum_Price': input['max_price'],
        'Full_Name': input['lead_name'],
        'Lead_Source': str(type)
    }

    if type(input['locality_name']) == str:
        data['Interested_Localities'] = [input['locality_name']]
    else:
        data['Interested_Localities'] = list(input['locality_name'])

    if input['service_type'] == 'new-projects':
        data['Interested_in_wf'] = 'New'
    
    return data


# MAPPING BULK DATA

def bulk_mapping(data):
    data = {
        'leadid': data['LEADID'][5:],
        'email': data['Email'],
        'phone': data['Phone'],
        'name': data['Full Name'],
        'project_enquired_for': data['Project Enquired for'],
        'interested_properties': data['Interested Properties']
    }
    return data


# SEND MAIL VIA MAILGUN

def send_mail(lead_id, path, sub_project_name, name1):
    import subprocess
    # EXAMPLE CURL
    # curl -s --user REDACTED_SECRET_7 https://api.mailgun.net/v3/REDACTED_MAILGUN_DOMAIN/messages -F from='Automation Error <mailgun@REDACTED_MAILGUN_DOMAIN>' -F to=redacted@example.com -F to=redacted@example.com -F subject="Error. Testing Test - Mithila" -F text="Error. Lead registration failure.Lead ID: 920786000201726133 Project: Mithila Name: Testing Test" -F attachment=@"./krishnagrp/Testing Test_+919098124992738_Krishna Mithila.png"
    Mailgun = {
        "MAILGUN_DOMAIN": "REDACTED_MAILGUN_DOMAIN",
        "MAILGUN_URL": "https://api.mailgun.net/v3/REDACTED_MAILGUN_DOMAIN/messages",
        "MAILGUN_KEY": "REDACTED_SECRET_8",
        "FROM_MAIL": "mailgun@REDACTED_MAILGUN_DOMAIN",
        "TO_MAIL": ["redacted@example.com", "redacted@example.com"],
        # "TO_MAIL":["redacted@example.com","redacted@example.com"],
        "PASS": "REDACTED",
        "NAME": "Mailgun"
        }
    try:
        print("Sending mail...")
        subject = "Error. {} - {}".format(name1, sub_project_name)
        text = "Error. Lead registration failure. Lead ID: {} Project: {} Name: {}".format(lead_id, sub_project_name, name1)

        curlurl = "curl -s --user 'api:{}' {} -F from='Automation Error <mailgun@{}>' -F to={} -F to={} -F subject='{}' -F text='{}' -F attachment=@'{}'".format(Mailgun['MAILGUN_KEY'], Mailgun['MAILGUN_URL'], Mailgun['MAILGUN_DOMAIN'], Mailgun['TO_MAIL'][0], Mailgun['TO_MAIL'][1], subject, text, path)

        s, o = subprocess.getstatusoutput(curlurl)
        print(s, o, sep="\n")

    except Exception as e:
        print("Exception occured due to: ", str(e))
        print("Exception in sending mail...")

    return


# GET ACCESS TOKEN

def get_access_token():
    from requests.structures import CaseInsensitiveDict
    import os
    zoho = {
        "URL": "https://www.zohoapis.com/crm/v2/Leads/",
        "CLIENT_ID": "REDACTED",
        "CLIENT_SECRET": "REDACTED",
        "REFRESH_TOKEN": "REDACTED",
        "REDIRECT_URI": "https://example.com",
        "NAME": "Zoho"
        }

    try:
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
        # print(os.get(['access_token']))
    except Exception:
        try:
            access_token = os.environ.get("access_token")
            print(access_token)
        except Exception as e:
            print("Failed to create Access token. \n" + str(e))

    return access_token


# UPLOAD ATTACHMENT TO ZOHO

def upload_an_attachment(lead_id, path):
    import subprocess
    access_token = get_access_token()
    try:
        CurlUrl = "curl 'https://www.zohoapis.com/crm/v2/Leads/{}/Attachments' -X POST -H 'Authorization: Zoho-oauthtoken {}' -F 'file=@{}'".format(
            lead_id,
            access_token,
            path)
        out1, out2 = subprocess.getstatusoutput(CurlUrl)
        print(out1, out2)
    except Exception:
        print("Failed to Upload...")
    return


# SEARCH PROJECT ID

def getProjectID(project_name, access_token):
    url = 'https://www.zohoapis.com/crm/v2/Deals/search'
    params = {
        'fields': 'Deal_Name',
        'criteria': '(Deal_Name:starts_with:{})'.format(project_name)
    }
    headers = {
        'Authorization': 'Zoho-oauthtoken ' + str(access_token),
    }
    resp = get(url, params=params, headers=headers)

    if resp.status_code == 200:
        data = loads(resp.content)['data']
        if data:
            id = data[0]['id']
            return id

    return {'error': 'No such project'}


# INSERT NEW RECORD IN ZOHO

def insert_records(record, access_token):
    url = 'https://www.zohoapis.com/crm/v2/Leads/upsert'
    headers = {
        'Authorization': 'Zoho-oauthtoken ' + str(access_token),
    }
    request_body = dict()
    record_list = list()
    duplicate_check_fields= ["Email", "Phone"]
    trigger = ["workflow"]
    record_list.append(record)
    request_body['data'] = record_list
    request_body['duplicate_check_fields'] = duplicate_check_fields
    request_body['trigger'] = trigger
    response = post(url=url, headers=headers, data=dumps(request_body).encode('utf-8'))
    if response is not None:
        print("HTTP Status Code : " + str(response.status_code))
        print(response.json())
        return response.json()
    return {'status': 'Failed'}


# MAIN FUNCTION FOR INSERT RECORD

def insert_record_to_zoho(record, type = None):
    print('insert_record_to_zoho', type)
    if not type:
        access_token = get_access_token()
        print(access_token)
        id = getProjectID(record['project_name'], access_token)
        print(record['project_name'], 'id: ', id)
        if 'error' not in id:
            data = mapping(record, id)
            print(data)
            response = insert_records(data, access_token)
            print(response)
            return response
    elif type == 'housing':
        access_token = get_access_token()
        print(access_token)
        id = getProjectID(record['project_name'], access_token)
        print(record['project_name'], id)
        if 'error' not in id:
            data = mapping(record, id, type = 'Housing automation')
            print(data)
            response = insert_records(data, access_token)
            print(response)
            return response
    elif type == 'magicbricks':
        access_token = get_access_token()
        response = insert_records(data, access_token)
        return response
    return {'status': 'success'}


# INSERT RECORD FROM HOUSING API

def housing_api():
    try:
        import requests
        import hmac
        import hashlib
        from datetime import datetime, timedelta
        import time
        import pytz

        print('Housing')

        date_time = datetime.now()
        date_time = pytz.utc.localize(date_time)
        timestamp = int(time.mktime(date_time.timetuple()))

        today = datetime.today() + timedelta(days=1)
        yesterday = today - timedelta(days=2)

        yesterday = pytz.utc.localize(yesterday)
        today = pytz.utc.localize(today)

        yesterday = int(time.mktime(yesterday.timetuple()))
        today = int(time.mktime(today.timetuple()))

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
                response = insert_record_to_zoho(record, type = 'housing')
                logs.append(response)
            except Exception as e:
                logs.append(str(e))
        return logs

    except Exception as e:
        return {'error': str(e)}


# INSERT RECORD FROM MAGICBRICKS API

def magicbricks_api():
    try:
        import requests
        from datetime import datetime, timedelta
        import pytz
        from json import loads

        print('Magicbricks')

        today = datetime.today() + timedelta(days=1)
        yesterday = today - timedelta(days=2)

        yesterday = pytz.utc.localize(yesterday)
        today = pytz.utc.localize(today)

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
                print(access_token)
                project_id = getProjectID(input['project'], access_token)
                print('project_id: ', project_id)
                apartment_names = '2 BHK'
                if '4 BHK' in input['msg']:
                    apartment_names = '4 BHK'
                elif '3 BHK' in input['msg']:
                    apartment_names = '3 BHK'
                data = {
                    'Configuration1': apartment_names,
                    'Country_Code': '+' + str(input['isd']),
                    'Interested_Localities': input['locality'],
                    'City': input['city'],
                    'Email': input['email'],
                    'Phone': input['mobile'],
                    'Project_Enquired_for': dict({'id': project_id}),
                    'Full_Name': input['name'],
                    'Automation Updates': str('Subject: ') + str(input['subject']) + str('\n\n') + str('Message: ') + str(input['msg']) + str('\n\n') + str(input),
                    'Lead_Source': 'magicbricks_automation'
                }
                print(data)
                response = insert_records(data, access_token)
                print(response)
                logs.append(response)
            except Exception as e:
                logs.append(str(e))
        
        return logs
    
    except Exception as e:
        return {'error': str(e)}