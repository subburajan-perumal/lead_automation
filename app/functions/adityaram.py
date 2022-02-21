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

        if sub_project_name == "Adityaram Nagar Phase 5":
            sub_project_name = "Adityaram Nagar 5"
        if sub_project_name == "Adityaram":
            sub_project_name = "Adityaram Signature City"        
        if sub_project_name == "Adityaram Signature City":
            sub_project_name = "Adityaram Signature City"
        
        
    #browser# yield "on working"
        save_path=getsavePath(path,sub_project_name)
        browser.get(SITE["url"])
        f_name=browser.find_elements(By.XPATH,'/html/body/div[1]/div/form/div[2]/div/div/input')
        f_name[0].send_keys(fullname)
        #client email
        f_email=browser.find_elements(By.XPATH,'/html/body/div[1]/div/form/div[3]/div/div/input')
        f_email[0].send_keys(lead_data["email"])
        #client contact
        f_contact=browser.find_elements(By.XPATH,'/html/body/div[1]/div/form/div[4]/div/div/div/input')
        f_contact[0].send_keys(lead_data["phone"])
        #CPname
        f_cpname=Select(browser.find_element(By.XPATH,'/html/body/div[1]/div/form/div[5]/div[1]/div/select'))
        f_cpname.select_by_visible_text(SITE["cpname"])
        #CPphone
        f_cpphn1=browser.find_elements(By.XPATH,'/html/body/div[1]/div/form/div[5]/div[2]/div/input')
        f_cpphn1[0].send_keys(SITE["cpphn"])
        #Project
        f_project=Select(browser.find_element(By.XPATH,'/html/body/div[1]/div/form/div[6]/div/div/select'))
        f_project.select_by_visible_text(sub_project_name)
        time.sleep(3)

        browser.save_screenshot(save_path[0])    

        f_add=browser.find_element(By.XPATH,'/html/body/div[1]/div/form/div[8]/div/div/input').click()
        time.sleep(5)

        browser.save_screenshot(save_path[1])    
        browser.close()        

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