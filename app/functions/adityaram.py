from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import NoSuchElementException
from pymongo import MongoClient
import app.functions.common_util as commonutil
from app.util.utility import getTime,getsavePath
from datetime import datetime
import app.functions.Config as Config
import time
import os

def addlead(project,sub_project_name,storage,**lead_data):
    #database
    SITE, LEADS = commonutil.projectCheck(project,sub_project_name,**lead_data)
    if SITE == -1:
        return "Failed"
    try:
        sub_project_name = Config.project_sub[sub_project_name]
        firefox_service=Service("./geckodriver")
        opt=Options()
        opt.headless=False
        browser=webdriver.Firefox(options=opt,service=firefox_service)
    
        site_name = SITE["name"]
        path = storage+site_name
        if not os.path.exists(path):
            os.mkdir(path)
        
        fullname = lead_data['first_name'] + ' ' + lead_data['last_name']

        
    #bro wser# yield "on working"
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
        lead_detail={"projectname":SITE['name'],
        "subproject":sub_project_name,
        "applied_time":datetime.now(),
        "status":req
        }
        LEADS.update_one({"email":lead_data["email"],"phone":lead_data["phone"]},{"$push":{"project":lead_detail}})
    
    except NoSuchElementException as nse:
        req="failed"
        browser.save_screenshot(save_path[2])
        browser.close()
        print("Error occured : ",str(nse))
        lead_detail={"projectname":SITE['name'],#akshaya
        "subproject":sub_project_name,#Tango
        "applied_time":datetime.now(),
        "status":req
        }
        LEADS.update_one({"email":lead_data["email"],"phone":lead_data["phone"]},{"$set":{"modified_time":datetime.now()},"$push":{"project":lead_detail}})

    except:
        browser.save_screenshot(save_path[2])
        req="failed"
        print('error occured')
    
    finally:
        return req