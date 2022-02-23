from importlib import import_module
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pymongo import MongoClient
from app.util.utility import getTime,getsavePath
from  datetime import datetime
import time
import os
import app.functions.common_util as commnutil
import app.functions.Config as Config
def addlead(project,sub_project_name,storage,**lead_data):
    #database
    try:
        print("alliance function working")
        SITE, LEADS = commnutil.dbcheck(project,sub_project_name,**lead_data)
        if SITE == -1:
            return "Failed"
        sub_project_name = Config.project_sub[sub_project_name]
        firefox_service=Service("./geckodriver")
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
        
        # browser=webdriver.Firefox(service=s)
        browser.get(SITE["url"])
        f_search=browser.find_element(By.ID,'email')
        f_search.send_keys(SITE["email"])
        f_password=browser.find_element(By.ID,'password')
        f_password.send_keys(SITE["pass"])
        f_submit=browser.find_element(By.ID,'digit_login_signin_submit')
        f_submit.send_keys(Keys.RETURN)
        time.sleep(10)
        f_lead=browser.find_elements(By.CLASS_NAME,'kt-menu__item')
        f_lead[1].click()
        time.sleep(5)
        f_name=browser.find_element(By.NAME,'name')
        f_name.send_keys(fullname)
        f_contact=browser.find_element(By.NAME,'contact')
        f_contact.send_keys(lead_data["phone"])
        f_email=browser.find_element(By.NAME,'email')
        f_email.send_keys(lead_data["email"])
        f_project=Select(browser.find_element(By.ID,'select_project'))
        f_project.select_by_visible_text(sub_project_name)

        browser.save_screenshot(save_path[0])    

        # f_add=browser.find_element(By.ID,'lead_submit_btn').click()
        # aa = WebDriverWait(browser, 10).until(
        #         EC.presence_of_element_located((By.XPATH,"//*[@id='kt_table_1']/tbody/tr[1]/td[7]"))
        # )
        # req=aa.text
        # aa.click()
        
        time.sleep(5) ## FOR CHANGING WAIT TIME
        browser.save_screenshot(save_path[1])
        browser.quit()


        print("\tSelenium working properly")
        req="success"
        lead_detail={"projectname":SITE['name'],
        "subproject":sub_project_name,
        "applied_time":datetime.now(),
        "status":req
        }
        LEADS.update_one({"email":lead_data["email"],"phone":lead_data["phone"]},{"$push":{"project":lead_detail}})
        
        print("lead uploaded")
    
    
    
    except:
        browser.save_screenshot(save_path[2])
        req="failed"
        print('error occured')
    
    finally:
        return req