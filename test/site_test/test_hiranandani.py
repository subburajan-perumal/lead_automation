
from asyncio import subprocess
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
from selenium.webdriver.support import expected_conditions as EC
from phonenumbers import geocoder as GC
import phonenumbers as PN
import time
import logging
logging.basicConfig(filename="execution.log",
    level=logging.INFO,
    format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s'
    )
browserLog=logging.getLogger("selenium_log")

# browserLog.setLevel=logging.INFO


driver="./geckodriver"
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
      "first_name": "subbu",
    "last_name": "Manikandan", 
    "email": "redacted@example.com", 
    "phone": "9000000000",
     "project_enquired_for": "",
      "interested_properties": "SPR Market of India", 
      "interested_localities": "Perambur",
       "initial_enquiry_particulars_automation": ""
    }

site_data={"_id":{"$oid":"623c25874dca8f32e9244181"},"name":"hiranandani","url":"https://hiranandaniparkschennai.com/channelpartners/","email":"LeadAutomation","pass":"REDACTED","partner_name":"Lead Automation","status":1,"project_list":[{"project_name":"Hiranandani Parks","keywords":["Hiranandani Parks","None (default)","Oragadam","VBHC","Shriram Shankari","Shriram Shankari lakeside","Lumina","HiranandaniTest"],"location":["Oragadam"]}]}


def hiranandani(subproject, browser, site_data, lead_data, path):
    try:
        browserLog.info("hiranandani started")
        save_path=path

        browser.get(site_data["url"])
        tem = browser.find_element(By.CLASS_NAME, 'reffer-btn').click()

        name  = browser.find_element(By.NAME, "Pname")
        name.send_keys(lead_data['name'])

        contact=browser.find_element(By.NAME,'pmob')
        contact.send_keys(lead_data['phone'])

        intrest_project = browser.find_element(By.NAME, 'interested')
        new = Select(intrest_project)
        new.select_by_index(2)

        email=browser.find_element(By.NAME,'pemail')
        email.send_keys(lead_data['email'])

        add=browser.find_element(By.XPATH,'/html/body/div[3]/div/div/div/form/div[1]/div/div/div[6]/div/div[2]/span/span').click()

        intrest_project = browser.find_element(By.NAME, 'cname')
        new = Select(intrest_project)
        new.select_by_index(13)      

        # browser.save_screenshot(save_path[0])
        browser.implicitly_wait(5)
        # browser.save_screenshot(save_path[1])
        time.sleep(10)
        browser.close()
        browserLog.info("hiranandani Executed Successfully")
        return 1

    except Exception as e:
        print(str(e))
        browserLog.info("hiranandani error occured")
        # browser.save_screenshot(save_path[2])
        return -1
subproject="Hiranandani Parks"
path="."
hiranandani(subproject, browser, site_data, lead_data, path)
