#error occur at the end of selenium

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
      "first_name": "subbu",
    "last_name": "Manikandan", 
    "email": "redacted@example.com", 
    "phone": "9000000000",
     "project_enquired_for": "",
      "interested_properties": "SPR Market of India", 
      "interested_localities": "Perambur",
       "initial_enquiry_particulars_automation": ""
    }
site_data={"_id":{"$oid":"623c25874dca8f32e924417f"},"name":"fomra","url":"http://www.fomrahousing.in/cp/?srd=5d1892be5e3c3067305fa1d2","channel_phone_number":"9000000000","partner_name":"Lead Automation","status":1,"project_list":[{"project_name":"Hues","keywords":["Fomra Hues","Green Enclave","Emerald Peninsula","Brigade Xanadu","Brigade Bonito","Signature City","FomraTest"],"location":[]},{"project_name":"Celebration","keywords":["Fomra Celebration"],"location":[]},{"project_name":"Vayou","keywords":["Fomra Vayou"],"location":[]}]}

def fomra(subproject:str, browser, site_data:dict, lead_data:dict, automate_path:list):
    try:
        browserLog.info("fomra started")
        save_path = automate_path
        fullname= str(lead_data['name'])
        #need to change with getName function
        first_name, last_name = lead_data["first_name"],lead_data["last_name"]
        browser.get(site_data['url'])
        f_name= browser.find_element(By.XPATH, '/html/body/div/div/div/div/div/div/div/form/div[2]/div/div/input[1]')
        f_name.send_keys(fullname)
        f_email= browser.find_element(By.XPATH, '/html/body/div/div/div/div/div/div/div/form/div[3]/div/div/input')
        f_email.send_keys(lead_data['email'])
        f_phone= browser.find_element(By.XPATH, '//html/body/div/div/div/div/div/div/div/form/div[4]/div/div/div/input')
        f_phone.send_keys(lead_data['phone'])
        f_project= Select(browser.find_element(By.XPATH, '/html/body/div/div/div/div/div/div/div/form/div[7]/div/div/select'))
        f_project.select_by_visible_text(site_data["partner_name"])
        
        f_channel_pn= Select(browser.find_element(By.XPATH, '/html/body/div/div/div/div/div/div/div/form/div[5]/div/div/select'))
        f_channel_pn.select_by_visible_text(subproject)
        
        f_channel_phone= browser.find_element(By.XPATH, '/html/body/div/div/div/div/div/div/div/form/div[8]/div/div/input')
        f_channel_phone.send_keys(site_data["channel_phone_number"])

        
        # browser.save_screenshot(save_path[0])    
    

        f_submit= browser.find_element(By.XPATH, '/html/body/div/div/div/div/div/div/div/form/div[9]/div/div/input').click()
        time.sleep(5)
        # browser.implicitly_wait(5)

        
        # browser.save_screenshot(save_path[1])
        browserLog.info("fomra executed successfully")
        browser.close()
        return 1
    except Exception as e:
        print(str(e))
        browserLog.error(" fomra Error occured ")
        time.sleep(2)
        # browser.save_screenshot(save_path[2])

        return -1

subproject="Hues"
path="."
fomra(subproject, browser, site_data, lead_data, path)