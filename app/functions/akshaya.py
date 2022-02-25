
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from pymongo import MongoClient
from app.util.utility import getTime,getsavePath
import time
import os
from datetime import datetime, timedelta
import app.functions.common_util as commnutil
import app.functions.Config as Config

# async def browsertimer(v_browser):
#     time.sleep(100)
#     v_browser.quit()

def addlead(project,sub_project_name,storage,**lead_data):
    try:
        SITE, LEADS = commnutil.projectCheck(project,sub_project_name,**lead_data)
        if SITE == -1:
            req="failed"
            return req

        sub_project_name = Config.project_sub[sub_project_name]
        firefox_service=Service("./geckodriver")
        opt=Options()
        opt.headless=False
        browser=webdriver.Firefox(options=opt,service=firefox_service)
        # browsertimer(browser)
        path = storage+SITE['name']
        if not os.path.exists(path):
            os.mkdir(path)
        
        fullname = lead_data['first_name'] + ' ' + lead_data['last_name']

        save_path=getsavePath(path,sub_project_name)
        
        
        print("\tSelenium started")
        browser.get(SITE["url"])
        f_email = browser.find_element(By.ID, "user_email")
        f_email.send_keys(SITE["email"])
        f_password = browser.find_element(By.ID,"user_password")
        f_password.send_keys(SITE["pass"])
        browser.find_element(By.XPATH,"//button[@type='submit']").click()

        f_Leads = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.LINK_TEXT, "Leads")))
        # f_Leads = browser.find_element(By.LINK_TEXT, "Leads")
        f_Leads.click()
        f_addlead = browser.find_element(By.XPATH, "//a[@href='/broker/2150/leads/new']")
        f_addlead.click()    
        f_firstname = browser.find_element(By.ID, "lead_first_name")
        f_firstname.send_keys(lead_data.get("first_name"))
        f_lastname = browser.find_element(By.ID, "lead_last_name")
        f_lastname.send_keys(lead_data.get("last_name"))
        f_mail = browser.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/form/div[2]/div[2]/div[2]/div[1]/div/div/a')
        f_mail.click()
        f_mail1 = browser.find_element(By.XPATH, '/html/body/div[3]/div/input')
        f_mail1.click()
        f_mail1.send_keys(lead_data.get("email"))
        f_mail1.send_keys(Keys.RETURN)
        f_phone = browser.find_element(By.XPATH, '//*[@id="lead_phone"]')
        f_phone.click()
        f_phone.send_keys(lead_data.get("phone"))
        f_button2 = browser.find_element(By.XPATH, '//*[@id="s2id_lead_project_ids"]/a/span[2]')
        f_button2.click()
        f_project1 = browser.find_element(By.XPATH, '/html/body/div[4]/div/input')
        f_project1.send_keys(sub_project_name)
        f_project1.send_keys(Keys.RETURN)
        
        
        browser.save_screenshot(save_path[0])
        
        time.sleep(5)
        browser.save_screenshot(save_path[1])
        browser.close()

        print("\tSelenium working properly")
        req="success"
        lead_detail={"projectname":SITE['name'],#akshaya
        "subproject":sub_project_name,#Tango
        "applied_time":datetime.now(),
        "status":req
        }
        LEADS.update_one({"email":lead_data["email"],"phone":lead_data["phone"]},{"$set":{"modified_time":datetime.now()},"$push":{"project":lead_detail}})
        
        print("lead uploaded")
    
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

    except Exception as e:
        req="failed"
        browser.save_screenshot(save_path[2])
        
        print(str(e))
        print('error occured')
    
    finally:
        return req