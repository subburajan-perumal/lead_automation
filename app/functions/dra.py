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
    print("dra")
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
        fl_email = browser.find_element(By.ID, "user_email")
        fl_email.send_keys(SITE["email"])
        fl_password = browser.find_element(By.ID,"user_password")
        fl_password.send_keys(SITE["pass"])
        browser.find_element(By.XPATH,"//button[@type='submit']").click()

        f_Leads = browser.find_element(By.LINK_TEXT, "Leads")
        f_Leads.click()
        f_addlead = browser.find_element(By.XPATH, "/html/body/div/div/div[1]/div/ul/li/ul/li[2]/a")
        f_addlead.click()

        f_firstname = browser.find_element(By.ID, "lead_first_name")
        f_firstname.send_keys(lead_data["first_name"])
        f_lastname = browser.find_element(By.ID, "lead_last_name")
        f_lastname.send_keys(lead_data["last_name"])

        #nri = browser.find_element(By.ID, "lead_nri")
        #nri.click()
        #nri.click()

        f_mail = browser.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/form/div[2]/div[2]/div[2]/div[1]/div/div/a')
        f_mail.click()
        f_mail1 = browser.find_element(By.XPATH, '/html/body/div[3]/div/input')
        f_mail1.click()
        f_mail1.send_keys(lead_data["email"])
        f_mail1.send_keys(Keys.RETURN)
        f_phone = browser.find_element(By.XPATH, '//*[@id="lead_phone"]')
        f_phone.click()
        f_phone.send_keys(lead_data["phone"])
        f_button2 = browser.find_element(By.XPATH, '//*[@id="s2id_lead_project_ids"]/a/span[2]')
        f_button2.click()
        f_project = browser.find_element(By.XPATH, '/html/body/div[4]/div/input')
        f_project.send_keys(sub_project_name)
        f_project.send_keys(Keys.RETURN)

        browser.save_screenshot(save_path[0])    

        f_save = browser.find_element(By.XPATH, '//*[@id="new_lead"]/div[6]/input')
        f_save.click()
        
        time.sleep(5)
        browser.save_screenshot(save_path[1]) 
        browser.close()        

        req = "Success"
        

        print("\tSelenium working properly")
        req="success"
        lead_detail={"projectname":SITE['name'],
        "subproject":sub_project_name,
        "applied_time":datetime.now(),
        "status":req
        }
        LEADS.update_one({"email":lead_data["email"]},{"$push":{"project":lead_detail}})
        print("lead uploaded")
    
    
    except Exception as e:
        browser.save_screenshot(save_path[2])
        req="failed"
        print('error occured',str(e))
    
    finally:
        return req