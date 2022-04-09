from selenium.webdriver import Firefox
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.alert import Alert
from phonenumbers import geocoder as GC
import phonenumbers as PN
import time

import logging
logging.basicConfig(filename="execution.log",
    level=logging.INFO,
    format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s'
    )
browserLog=logging.getLogger("browser_log.log")

# browserLog.setLevel=logging.INFO


driver="/home/subburaj/LEAD_AUTOMATION/lead_automation/geckodriver"
firefox_service = Service(driver)
opt = Options()
opt.add_argument ( "--incognito" )
browser = webdriver.Firefox ( 
                            options = opt ,
                            service = firefox_service,
                            # service_log_path=WEBDRIVER_LOG
                            )

lead_data={
    "lead_id": "920786000234230275",
     "name": "Manikandan",
      "first_name": "",
    "last_name": "Manikandan", 
    "email": "redacted@example.com", 
    "phone": "9000000000",
     "project_enquired_for": "",
      "interested_properties": "SPR Market of India", 
      "interested_localities": "Perambur",
       "initial_enquiry_particulars_automation": ""
    }

site_data = {"_id": {"$oid": "623c25874dca8f32e9244177"}, "name": "adityaram", "url": "http://www.adityaramproperties.com/channel-partner/index.html?srd=610a6509c825611af77aad37", "cpname": "Lead Automation", "cpphn": "9000000000", "status": 0, "project_list": [{"project_name": "Adityaram Nagar 5", "keywords": [
    "Adityaram Nagar Phase 5", "None (default)", "Hamlet", "Emerald Hamlet", "Sobha Gardenia", "House of Hiranandani", "Silver Springs", "AadityaramTest"], "location":[]}, {"project_name": "Adityaram Signature City", "keywords": ["Adityaram Signature City", "Adityaram", "OMR", "Sholinganallur", "Navalur", "Siruseri", "Kelambakkam"], "location":[]}, {"project_name": "Adityaram Superstar", "keywords": [], "location":[]}]}

def adityaram(subproject:str, browser:Firefox, site_data:dict, lead_data:dict, path:list) :
    try:
        browserLog.info("adityaram started")
        save_path= path

        browser.get(site_data["url"])
        #client name
        
        #client name
        name=browser.find_elements(By.XPATH,'/html/body/div[1]/div/div/div/div/div/div/form/div[2]/div/div/input[1]')
        name[0].send_keys(lead_data['name'])
        #client email
        email=browser.find_elements(By.XPATH,'/html/body/div[1]/div/div/div/div/div/div/form/div[3]/div/div/input')
        email[0].send_keys(lead_data['email'])
        #client contact
        contact=browser.find_elements(By.XPATH,'/html/body/div[1]/div/div/div/div/div/div/form/div[4]/div/div/div/input')
        contact[0].send_keys(lead_data['phone'])
        #CPname
        cpname1=Select(browser.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div/div/div/form/div[5]/div[1]/div/select'))
        cpname1.select_by_visible_text(site_data["cpname"])
        #CPphone
        cpphn1=browser.find_elements(By.XPATH,'/html/body/div[1]/div/div/div/div/div/div/form/div[5]/div[2]/div/input')
        cpphn1[0].send_keys(site_data["cpphn"])
        #Project
        proj1=Select(browser.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div/div/div/form/div[6]/div/div/select'))
        proj1.select_by_visible_text(subproject)
        time.sleep(3)


        add=browser.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div/div/div/form/div[8]/div/div/input').click()
        time.sleep(3)

        # browser.save_screenshot(save_path)    
        # browser.close()
        browserLog.info("adityaram executed successfully")

    except Exception as e:
        print(str(e))
        browserLog.info("exception occured")
        browserLog.error(str(e))
        # browser.save_screenshot(save_path[2])
        return -1

subproject="Adityaram Nagar 5"
path="."
result=adityaram(subproject, browser, site_data, lead_data, path) 
assert result==1,"test Success"