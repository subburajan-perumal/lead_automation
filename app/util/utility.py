from json import dumps, loads,json
import os
from datetime import datetime
import pytz
from requests import get, post
import pymongo
from bson import json_util, ObjectId

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


def getsavePath(path, site_name, sub_project_name, leadname):
# Connecting to Lead Automation MongoDB server to get filename(subname)
    client = pymongo.MongoClient("mongodb://REDACTED_MONGO_URI")
    db = client["lead_automation"]
    mycol = db["Site"]
    result = mycol.find({"project_list.project_name": sub_project_name})
    result = json.loads(json_util.dumps(result))

    for elem in result[0]["project_list"]:
        if elem["project_name"] == sub_project_name:
            subname = elem["filename"]    

    return [
        str(str(path) + '/' + "pre" + "_" + site_name + "_" + str(sub_project_name)+"_"+str(leadname).replace(" ", '_') + ".png"),
        str(str(path) + '/' + "post" + "_" + site_name + "_" + str(sub_project_name)+"_"+str(leadname).replace(" ", "_") + ".png"),
        str(str(path) + '/' + "err" + "_" + site_name + "_" + str(sub_project_name)+"_"+str(leadname).replace(" ", "_") + ".png"),
        str(str(path) + '/' + "pre" + "_" + str(subname) + ".png"),
        str(str(path) + '/' + "post" + "_" + str(subname) + ".png"),
        str(str(path) + '/' + "err" + "_" + str(subname) + ".png")
        ]
# print(getsavePath("akshaya","Tango"))+str(leadname).replace(" ","_")



def mapping(input, id):
    data = {
        'Configuration1': input['apartment_names'],
        'Country_Code': input['country_code'],
        'Zoning': input['category_type'],
        'Interested_Localities': list(input['locality_name']),
        'City': input['city_name'],
        'Email': input['lead_email'],
        'Phone': input['lead_phone'],
        'Project_Enquired_for': dict(
            {
            # 'name': input['project_name'], 
            # 'id': input['project_id'],
            'id': id
            }),
        # 'Project_Enquired_for': '$' + input['project_name'],
        'Property_Type1': input['property_field'],
        'Minimum_Price': input['min_price'],
        'Maximum_Price': input['max_price'],
        'Full_Name': input['lead_name']
    }

    if input['service_type'] == 'new-projects':
        data['Interested_in_wf'] = 'New'
    
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
    
    return {'status': 'success'}


# MAIN FUNCTION FOR INSERT RECORD

def insert_record_to_zoho(record, type = None):
    access_token = get_access_token()
    id = getProjectID(input['project_name'], access_token)
    data = mapping(record, id)
    insert_records(data, access_token)
    return {'status': 'success'}