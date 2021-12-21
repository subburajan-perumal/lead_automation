from data import constants 

### GET CURRENT TIME
def getTime():
    from datetime import datetime
    import pytz
    now = datetime.now(pytz.timezone('Asia/Kolkata')) 
    print("now =", now)
    # dd/mm/YY H:M:S
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    return dt_string


### MAILGUN TO USER
def send_complex_message(lead_id, path):
    '''
    import requests
    return requests.post(
    constants.mailgun['MAILGUN_URL'],
    auth=("api", constants.mailgun['MAILGUN_KEY']),
    files = [("attachment", path)],
    data={
        "subject": "My subject",
        "from": constants.mailgun['from_mail'],
        "to": constants.mailgun['to_mail'],
        "text": "The text",
        "html": "The<br>html"
    },
    headers={'Content-type': 'multipart/form-data;'},
    )
    '''
    return


### CURL REQUEST
#### curl "https://www.zohoapis.com/crm/v2/Leads/920786000201361001/Attachments" -X POST -H "Authorization: Zoho-oauthtoken 1000.35725cfabfd50fa3fd09fa36e8c9c43b.ce104a47b0648225132cf5dc9ec52baa" -F "file=@test.jpg"


def upload_an_attachment_zoho(lead_id, path):
    import subprocess
    #import ast

    try:
        curl1 = "curl 'https://accounts.zoho.com/oauth/v2/token?client_id={}&client_secret={}&refresh_token={}&grant_type=refresh_token' -X POST".format(
        constants.zoho['client_id'], 
        constants.zoho['client_secret'], 
        constants.zoho['refresh_token'])
        print("Calling...." + str(curl1))
        status, output = subprocess.getstatusoutput(curl1)
        print('--------------------------------')
        print(status)
        print('--------------------------------')
        print(output)
        print('--------------------------------')
        output_str = str(output).split("\"")
        print(output_str)
        idx = output_str.index('access_token')
        print(output_str[idx+2])
        #output_json = ast.literal_eval(output_str)
        #print(output_json)
        access_token = output_str[idx+2]
        print("Access Token: " + str(access_token))
        print('--------------------------------')
        
    except Exception as e:
        print("Failed to create Access token. \n" + str(e))

    try:
        CurlUrl = "curl 'https://www.zohoapis.com/crm/v2/Leads/{}/Attachments' -X POST -H 'Authorization: Zoho-oauthtoken {}' -F 'file=@{}'".format(lead_id, access_token, path)
        status, output = subprocess.getstatusoutput(CurlUrl)
        print(CurlUrl)
        print('--------------------------------')
        print(status)
        print('--------------------------------')
        print(output)  
        print('--------------------------------')

    except:
        print("Failed to Upload...")  

    return


def upload_an_attachment(lead_id, path):
    
    upload_an_attachment_zoho(lead_id, path)
    send_complex_message(lead_id, path)        
    return


