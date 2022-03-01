def cmpstring(string1,string2):
    str1="".join([i for i in string1 if i.isalpha()])
    str2="".join([i for i in string2 if i.isalpha()])
    return str1==str2


def getTime():
            from datetime import datetime
            import pytz
            now = datetime.now(pytz.timezone('Asia/Kolkata')) 
            #print("now =", now)
            # dd/mm/YY H:M:S
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            return dt_string

            
def getName(name):
    splited_name=name.split(" ")
    
    if len(splited_name)==1:

        return([splited_name[0],splited_name[0]])
    elif len(splited_name)==2:
        return([splited_name])
    elif len(splited_name)==3:
        return([splited_name[0]+splited_name[1],splited_name[2]])
    else:
        return name
            
#pre_akshaya_Adityaram_phase_5_krishnamoorthy perumal.png
#(site,sub_projectname,path,leadname)
def getsavePath(path,site_name,sub_project_name,leadname):
    from datetime import date
    # today = date.today()
# ddmmYY
    # formateddate = today.strftime("%d%m%y")
    # print("d1 =", d1)

    return [str(str(path) + '/' + "pre" + "_" + site_name + "_" + str(sub_project_name)+"_"+str(leadname) + ".png"), 
    str(str(path) + '/' + "post" + "_" + site_name + "_" + str(sub_project_name)+"_"+str(leadname) + ".png"),
    str(str(path) + '/' + "err" + "_" + site_name + "_" + str(sub_project_name) + ".png")
    ]
# print(getsavePath("akshaya","Tango"))



def send_mail(lead_id, path, sub_project_name, name1):
    import subprocess
    ### EXAMPLE CURL
    # curl -s --user REDACTED_SECRET_7 https://api.mailgun.net/v3/REDACTED_MAILGUN_DOMAIN/messages -F from='Automation Error <mailgun@REDACTED_MAILGUN_DOMAIN>' -F to=redacted@example.com -F to=redacted@example.com -F subject="Error. Testing Test - Mithila" -F text="Error. Lead registration failure.Lead ID: 920786000201726133 Project: Mithila Name: Testing Test" -F attachment=@"./krishnagrp/Testing Test_+919098124992738_Krishna Mithila.png"
    Mailgun={"MAILGUN_DOMAIN":"REDACTED_MAILGUN_DOMAIN",
"MAILGUN_URL":"https://api.mailgun.net/v3/REDACTED_MAILGUN_DOMAIN/messages",
"MAILGUN_KEY":"REDACTED_SECRET_8",
"FROM_MAIL":"mailgun@REDACTED_MAILGUN_DOMAIN",
"TO_MAIL":["redacted@example.com","redacted@example.com"],
"PASS":"REDACTED",
"NAME":"Mailgun"}
    try:
        print("Sending mail...")
        subject = "Error. {} - {}".format(name1, sub_project_name) 
        text = "Error. Lead registration failure. Lead ID: {} Project: {} Name: {}".format(lead_id, sub_project_name, name1)
        
        curlurl = "curl -s --user 'api:{}' {} -F from='Automation Error <mailgun@{}>' -F to={} -F to={} -F subject='{}' -F text='{}' -F attachment=@'{}'".format(Mailgun['MAILGUN_KEY'], Mailgun['MAILGUN_URL'],Mailgun['MAILGUN_DOMAIN'], Mailgun['to_mail'][0], Mailgun['to_mail'][1], subject, text, path)
        
        s , o = subprocess.getstatusoutput(curlurl)

    except:
        print("Exception in sending mail...")
    
    return

def upload_an_attachment(lead_id, path):
    import requests
    from requests.structures import CaseInsensitiveDict
    import subprocess
    import os

    zoho={"URL":"https://www.zohoapis.com/crm/v2/Leads/",
    "CLIENT_ID":"REDACTED",
    "CLIENT_SECRET":"REDACTED",
    "REFRESH_TOKEN":"REDACTED",
    "REDIRECT_URI":"https://example.com",
    "NAME":"Zoho"}
    try:
        url = 'https://accounts.zoho.com/oauth/v2/token?client_id={}&client_secret={}&refresh_token={}&grant_type=refresh_token'.format(
        zoho['CLIENT_ID'], 
        zoho['CLIENT_SECRET'], 
        zoho["REFRESH_TOKEN"])

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