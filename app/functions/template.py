from importlib import import_module
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from pymongo import MongoClient
from app.util.utility import getTime,getsavePath
import time
import os

def addlead(project,sub_project_name,storage,**lead_data):
    #database
    print("function working")
    try:
        CONN=MongoClient("mongodb://REDACTED_MONGO_URI")
        DB = CONN['lead_automation']
        LEADS=DB['leads']
        SITE=DB['Site'].find_one({"name":project})
        print(SITE['name'])
        print("db working")
        
    except Exception as e:
        print("Error occured due to "+str(e))
    try:
        
        firefox_service=Service("/home/subburaj/LEAD_AUTOMATION/lead_automation/geckodriver")
        opt=Options()
        opt.headless=False
        browser=webdriver.Firefox(options=opt,service=firefox_service)
    except:
        print("browser not working")
    
    try:
        site_name = SITE["name"]
        path = storage+site_name
        if not os.path.exists(path):
            os.mkdir(path)
        
        fullname = lead_data['first_name'] + ' ' + lead_data['last_name']

        
        
    #browser# yield "on working"
        save_path=getsavePath(path,sub_project_name)
        
        

        print("\tSelenium working properly")
        req="success"
        s_leads={"name":fullname,
        "project_name":sub_project_name,
        "phone":lead_data["phone"],
        "email":lead_data["email"],
        "status":req,
        "created_at":getTime()}
        LEADS.insert_one(s_leads)
        print("lead uploaded")
    
    
    except:
        browser.save_screenshot(save_path[2])
        req="failed"
        print('error occured')
    
    finally:
        return req