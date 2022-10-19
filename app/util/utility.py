from json import dumps, loads
from datetime import datetime
import json
from uuid import uuid4
import pytz
from requests import get, post
import pymongo
from bson import json_util
from celery.utils.log import get_task_logger
import os
import requests

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
        str(str(path2) + '/' + "pre" + "_" + str(subname) +"_"+ str(uuid4().hex) + ".png"),
        str(str(path2) + '/' + "post" + "_" + str(subname) +"_" + str(uuid4().hex) + ".png"),
        str(str(path2) + '/' + "err" + "_" + str(subname) +"_" + str(uuid4().hex) + ".png")
        ]


# MAPPING BULK DATA

def bulk_mapping(data):
    data['Phone'] = '+' + str(data['Phone'])
    if 'Email' not in data:
        data['Email'] = data['Phone'] + '@example.com'
    data = {
        'lead_id': data['LEADID'][5:],
        'email': data['Email'],
        'phone': data['Phone'],
        'mobile': data['Phone'],
        'alt_phone': data['Phone'],
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
    from dotenv import load_dotenv, find_dotenv, get_key
    dotenv_file = find_dotenv()
    load_dotenv(dotenv_file)
    access_token = get_key(dotenv_file, 'access_token', encoding='utf-8')
    return access_token


# UPLOAD ATTACHMENT TO ZOHO

def upload_an_attachment(lead_id, path):
    print('Upload attachment: {}, {}'.format(lead_id, path))
    import subprocess
    access_token = get_access_token()
    print('Access token: {}'.format(access_token))
    try:

        url = 'https://www.zohoapis.com/crm/v2/Leads/{}/Attachments'.format(lead_id)

        headers = {
            'Authorization': 'Zoho-oauthtoken {}'.format(access_token)
        }

        fullpath = path
        path, filename = os.path.split(fullpath)
        root, ext = os.path.splitext(filename)
        the_rest = root.rsplit("_", 1)

        filename = the_rest[0] + ext

        files=[
            ('file',(filename,open(fullpath,'rb'),'image/png'))
            ]

        response = requests.post(url=url, files=files, headers=headers)

        if response is not None:
                print("HTTP Status Code : " + str(response.status_code))

                print(response.json())
        # CurlUrl = "curl 'https://www.zohoapis.com/crm/v2/Leads/{}/Attachments' -X POST -H 'Authorization: Zoho-oauthtoken {}' -F 'file=@{}'".format(
        #     lead_id,
        #     access_token,
        #     path)
        # out1, out2 = subprocess.getstatusoutput(CurlUrl)
        # print(out1, out2)
    except Exception:
        print("Failed to Upload...")
    return


# SEARCH PROJECT ID
'''
def getProjectID(project_name, access_token):
    url = 'https://www.zohoapis.com/crm/v3/coql'
    # data = "{\r\n \"select_query\": \"select id from Deals where Deal_Name like '{}' limit 1\"\r\n}".format(project_name)
    data = {
        "select_query": "select id from Deals where Deal_Name like '{}' limit 1".format(project_name)
    }
    headers = {
        'Authorization': 'Zoho-oauthtoken ' + str(access_token),
    }
    resp = post(url, data=json.dumps(data), headers=headers)

    print('getProjectID')
    print(resp.content)
    try:
        print(resp.request)
    except:
        pass

    if resp.status_code == 200:
        data = loads(resp.content)['data']
        if data:
            id = data[0]['id']
            return id

    return {'error': 'No such project'}
'''


# SEARCH PROJECT ID

def getProjectID(project_name, access_token):
    url = 'https://www.zohoapis.com/crm/v2/Deals/search'
    params = {
        'fields': 'Deal_Name',
        'criteria': '(Deal_Name:starts_with:{})or(Project_Alias_2:starts_with:{})or(Project_Alias:starts_with:{})'.format(project_name,project_name,project_name)
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
        return {'response' : str(response.content), 'status_code': response.status_code}
    
    return {'status': 'Failed'}