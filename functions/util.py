from data import constants 

### GET CURRENT TIME
def getTime():
    from datetime import datetime
    import pytz
    now = datetime.now(pytz.timezone('Asia/Kolkata')) 
    #print("now =", now)
    # dd/mm/YY H:M:S
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    return dt_string


def send_mail(lead_id, path, sub_project_name, name1):
    import subprocess
    ### EXAMPLE CURL
    # curl -s --user REDACTED_SECRET_7 https://api.mailgun.net/v3/REDACTED_MAILGUN_DOMAIN/messages -F from='Automation Error <mailgun@REDACTED_MAILGUN_DOMAIN>' -F to=redacted@example.com -F to=redacted@example.com -F subject="Error. Testing Test - Mithila" -F text="Error. Lead registration failure.Lead ID: 920786000201726133 Project: Mithila Name: Testing Test" -F attachment=@"./krishnagrp/Testing Test_+919098124992738_Krishna Mithila.png"

    try:
        print("Sending mail...")
        subject = "Error. {} - {}".format(name1, sub_project_name) 
        text = "Error. Lead registration failure. Lead ID: {} Project: {} Name: {}".format(lead_id, sub_project_name, name1)
        
        curlurl = "curl -s --user 'api:{}' {} -F from='Automation Error <mailgun@{}>' -F to={} -F to={} -F subject='{}' -F text='{}' -F attachment=@'{}'".format(constants.mailgun['MAILGUN_KEY'], constants.mailgun['MAILGUN_URL'], constants.mailgun['MAILGUN_DOMAIN'], constants.mailgun['to_mail'][0], constants.mailgun['to_mail'][1], subject, text, path)
        
        s , o = subprocess.getstatusoutput(curlurl)

    except:
        print("Exception in sending mail...")
    
    return

def upload_an_attachment(lead_id, path):
    import requests
    from requests.structures import CaseInsensitiveDict
    import subprocess
    import os

    try:
        url = 'https://accounts.zoho.com/oauth/v2/token?client_id={}&client_secret={}&refresh_token={}&grant_type=refresh_token'.format(
        constants.zoho['client_id'], 
        constants.zoho['client_secret'], 
        constants.zoho['refresh_token'])

        headers = CaseInsensitiveDict()
        headers["Content-Length"] = "0"
        resp = requests.post(url, headers=headers)
        output = resp.json()
        access_token = output['access_token']
        os.environ["access_token"] = str(access_token)

    except:
        try:
            access_token = os.environ.get("access_token")

        except Exception as e:
            print("Failed to create Access token. \n" + str(e))

    try:
        CurlUrl = "curl 'https://www.zohoapis.com/crm/v2/Leads/{}/Attachments' -X POST -H 'Authorization: Zoho-oauthtoken {}' -F 'file=@{}'".format(lead_id, access_token, path)
        _, _ = subprocess.getstatusoutput(CurlUrl)

    except:
        print("Failed to Upload...")  

    return


### GET IMAGE SAVE PATHS
def getsavePath(path, name1, phone, sub_project_name):
    return [str(str(path) + '/' + str(sub_project_name) + str(name1) + "_post.png"), 
    str(str(path) + '/' + str(sub_project_name) + str(name1) + "_pre.png"),
    str(str(path) + '/' + str(sub_project_name) + str(name1) + "_error.png")
    ]