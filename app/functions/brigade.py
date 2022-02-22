from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from pymongo import MongoClient
from app.util.utility import getTime,getsavePath
from datetime import datetime
import time
import os
import app.functions.common_util as commonutil
import app.functions.Config as Config


def addlead(project,sub_project_name,storage,**lead_data):
    #database
    # print("brigade")
    try:
        SITE, LEADS = commonutil.dbcheck(project,sub_project_name,**lead_data)
        if SITE == -1:
            req="failed"
            return req
        sub_project_name = Config.project_sub[sub_project_name]
        firefox_service=Service("/home/subburaj/LEAD_AUTOMATION/lead_automation/geckodriver")
        opt=Options()
        opt.headless=False
        browser=webdriver.Firefox(options=opt,service=firefox_service)
    
        site_name = SITE["name"]
        path = storage+site_name
        if not os.path.exists(path):
            os.mkdir(path)
        
        fullname = lead_data['first_name'] + ' ' + lead_data['last_name']
        
        
        
    #browser# yield "on working"
        save_path=getsavePath(path,sub_project_name)
        browser.get(SITE["url"])
        company_name = browser.find_element(By.XPATH,'//*[@id="input_5"]')
        company_name.send_keys(SITE["company"])
        #agent name
        f_agentf = browser.find_elements(By.XPATH,'//*[@id="first_6"]')
        f_agentf[0].send_keys(SITE["agentf1"])
        f_agentl = browser.find_elements(By.XPATH,'//*[@id="last_6"]')
        f_agentl[0].send_keys(SITE["agentl1"])
        
        #agent mobile number
        f_aph11 = browser.find_elements(By.XPATH,'//*[@id="input_7_country"]')
        f_aph11[0].send_keys(SITE["aph1"])
        f_aph21 = browser.find_elements(By.XPATH,'//*[@id="input_7_area"]')
        f_aph21[0].send_keys(SITE["aph2"])
        f_aph31 = browser.find_elements(By.XPATH,'//*[@id="input_7_phone"]')
        f_aph31[0].send_keys(SITE["aph3"])
        
        #agent email
        f_mail = browser.find_elements(By.XPATH,'//*[@id="input_8"]')
        f_mail[0].send_keys(SITE["email"])
        
        #client name
        f_firstname=browser.find_element(By.XPATH,'//*[@id="first_11"]')
        f_firstname.send_keys(lead_data['first_name'])
        f_lastname = browser.find_element(By.ID,'last_11')
        f_lastname.send_keys(lead_data['last_name'])
        
        #mobile number 1
        f_aph1c = browser.find_element(By.XPATH,'//*[@id="input_12_country"]')
        f_aph1c.send_keys(SITE["aph1"])
        f_aph2c = browser.find_element(By.XPATH,'//*[@id="input_12_area"]')
        f_aph2c.send_keys(SITE["aph2"])
        f_aph3c = browser.find_element(By.XPATH,'//*[@id="input_12_phone"]')
        f_aph3c.send_keys(lead_data["phone"])
        
        #mobile number 2
        f_aph1c2 = browser.find_element(By.XPATH,'//*[@id="input_14_country"]')
        f_aph1c2.send_keys(SITE["aph1"])
        f_aph2c2 = browser.find_element(By.XPATH,'//*[@id="input_14_area"]')
        f_aph2c2.send_keys(SITE["aph2"])
        f_aph3c2 = browser.find_element(By.XPATH,'//*[@id="input_14_phone"]')
        f_aph3c2.send_keys(lead_data["phone"])
        
        #emails
        f_email11=browser.find_element(By.XPATH,'//*[@id="input_13"]')
        f_email11.send_keys(lead_data["email"])
        f_email21=browser.find_element(By.XPATH,'//*[@id="input_15"]')
        f_email21.send_keys(lead_data["email"])
        
        #project name
        project=Select(browser.find_element(By.XPATH,'//*[@id="input_16"]'))
        project.select_by_visible_text(sub_project_name)

        browser.save_screenshot(save_path[0])    

        # f_add=browser.find_element(By.XPATH,'//*[@id="input_2"]').click()
        
        time.sleep(10)
        browser.save_screenshot(save_path[1])
        browser.close()

        req = "Success"
        

        print("\tSelenium working properly")
        
        lead_detail={"projectname":SITE['name'],
        "subproject":sub_project_name,
        "applied_time":datetime.now(),
        "status":req
        }
        LEADS.update_one({"email":lead_data["email"]},{"$push":{"project":lead_detail}})
        print("lead uploaded")
    
    
    except:
        browser.save_screenshot(save_path[2])
        req="failed"
        print('error occured')
    
    finally:
        return req