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
from datetime import datetime
import app.functions.common_util as commonutil
import app.functions.Config as Config
def addlead(project,sub_project_name,storage,**lead_data):
    #database
    try:
        SITE, LEADS = commonutil.dbcheck(project,sub_project_name,**lead_data)
        if SITE == -1:
            req="failed"
            return req
    
        sub_project_name = Config.project_sub[sub_project_name]
        firefox_service=Service("./geckodriver")
        opt=Options()
        opt.headless=True
        browser=webdriver.Firefox(options=opt,service=firefox_service)
        site_name = "fomra"
        path = storage+SITE['name']
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
        lead_detail={"projectname":SITE['name'],
        "subproject":sub_project_name,
        "applied_time":datetime.now(),
        "status":req
        }
        LEADS.update_one({"email":lead_data["email"],"phone":lead_data["phone"]},{"$set":{"modified_time":datetime.now()},"$push":{"project":lead_detail}})
        
        print("lead uploaded")
    
    
    except:
        browser.save_screenshot(save_path[2])
        req="failed"
        print('error occured')
    
    
    finally:
        return req