from importlib import import_module
from re import S, sub
import re
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
    try:
        CONN=MongoClient("mongodb://REDACTED_MONGO_URI")
        DB = CONN['lead_automation']
        LEADS=DB['leads']
        SITE=DB['Site'].find_one({"name":project})
        print(SITE['name'])
        print("db working")
        
        firefox_service=Service("/home/subburaj/LEAD_AUTOMATION/lead_automation/geckodriver")
        opt=Options()
        opt.headless=True
        browser=webdriver.Firefox(options=opt,service=firefox_service)
        print("db driver working")
        site_name = "fomra"
        path = storage+site_name
        print("problem in create path")
        if not os.path.exists(str(path)):
            os.mkdir(path)
        fullname = lead_data['first_name'] + ' ' + lead_data['last_name']
        print("name convertion work")
        if sub_project_name == "Fomra Hues":
            sub_project_name = 'Hues'
        if sub_project_name == "Fomra Celebration":
            sub_project_name = 'Celebration'
        if sub_project_name == "Fomra Vayou":
            sub_project_name = 'Vayou'
        save_path=getsavePath(path,sub_project_name)
        #browser# yield "on working"
        # save_path=getsavePath(path,sub_project_name)
        
        print("\tSelenium started")
        browser.get(SITE['url'])
        f_name=browser.find_element(By.XPATH,'/html/body/div/div/div/div/div/div/div/form/div[2]/div/div/input[1]')
        f_name.send_keys(fullname)
        f_email=browser.find_element(By.XPATH,'/html/body/div/div/div/div/div/div/div/form/div[3]/div/div/input')
        f_email.send_keys(lead_data['email'])
        f_phone=browser.find_element(By.XPATH,'//html/body/div/div/div/div/div/div/div/form/div[4]/div/div/div/input')
        f_phone.send_keys(lead_data['phone'])
        f_project=Select(browser.find_element(By.XPATH,'/html/body/div/div/div/div/div/div/div/form/div[7]/div/div/select'))
        f_project.select_by_visible_text(SITE["partner_name"])
        
        f_channel_pn=Select(browser.find_element(By.XPATH,'/html/body/div/div/div/div/div/div/div/form/div[5]/div/div/select'))
        f_channel_pn.select_by_visible_text(sub_project_name)
        
        f_channel_phone=browser.find_element(By.XPATH,'/html/body/div/div/div/div/div/div/div/form/div[8]/div/div/input')
        f_channel_phone.send_keys(SITE["channel_phone_number"])

        
        browser.save_screenshot(save_path[0])    
        # upload_an_attachment(lead_id, save_path1)

        # submit=browser.find_element(By.XPATH,'/html/body/div/div/div/div/div/div/div/form/div[9]/div/div/input').click()
        time.sleep(10)

        print('success')
        browser.save_screenshot(save_path[1])
        browser.close()
        req="success"
        s_leads={"name":fullname,
        "project_name":sub_project_name,
        "phone":lead_data["phone"],
        "status":req,
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