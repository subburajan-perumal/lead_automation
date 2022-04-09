
from sqlite3 import SQLITE_DROP_TABLE
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

site_data={"_id":{"$oid":"623c25874dca8f32e924417e"},"name":"dra","url":"http://cp.sell.do/users/sign_in","email":"redacted@example.com","pass":"REDACTED","status":1,"project_list":[{"project_name":"D'Elite","keywords":["Courtyards","Amethyst","Radiance Sapphire","D Lite","D ELite","Savoye","Risington","Godrej Azure","Olympia Opaline","DRA DeLite","TCP Altura","Elevate 21","Sholinganallur"],"location":["Sholinganallur"]},{"project_name":"Centralia","keywords":["DRA Centralia","Anchorage","Godrej Azure","Olympia Opaline","Akshaya OrlandO","Akshaya Today","OMR","Navalur","Siruseri","Kelambakkam","DRATest"],"location":["OMR","Navalur","Siruseri","Kelambakkam"]},{"project_name":"Truliv Navalur","keywords":["DRA Truliv Navalur"],"location":[]},{"project_name":"Truliv Navalur Commercial","keywords":["DRA Truliv Navalur Commercial"],"location":[]},{"project_name":"Truliv Porur","keywords":["DRA Truliv Porur","Porur","Green Enclave","Emerald Peninsula","Signature City"],"location":[]},{"project_name":"90 Degrees","keywords":[],"location":[]},{"project_name":"ASCOT","keywords":[],"location":[]},{"project_name":"Tuxedo Elite","keywords":[],"location":[]}]}

def dra(subproject, browser, site_data, lead_data, path):
    try:
        browserLog.info("dra started")
        save_path=path

        browser.get(site_data["url"])
        email = browser.find_element(By.ID, "user_email")
        email.send_keys(site_data["email"])
        password = browser.find_element(By.ID,"user_password")
        password.send_keys(site_data["pass"])
        browser.find_element(By.XPATH,"//button[@type='submit']").click()

        Leads = browser.find_element(By.LINK_TEXT, "Leads")
        Leads.click()
        addlead = browser.find_element(By.XPATH, "/html/body/div/div/div[1]/div/ul/li/ul/li[2]/a")
        addlead.click()

        firstname = browser.find_element(By.ID, "lead_first_name")
        firstname.send_keys(lead_data['name'])
        lastname = browser.find_element(By.ID, "lead_last_name")
        lastname.send_keys(lead_data['name'])

        #nri = browser.find_element(By.ID, "lead_nri")
        #nri.click()
        #nri.click()

        mail = browser.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/form/div[2]/div[2]/div[2]/div[1]/div/div/a')
        mail.click()
        mail1 = browser.find_element(By.XPATH, '/html/body/div[3]/div/input')
        mail1.click()
        mail1.send_keys(lead_data['email'])
        mail1.send_keys(Keys.RETURN)
        phone1 = browser.find_element(By.XPATH, '//*[@id="lead_phone"]')
        phone1.click()
        phone1.send_keys(lead_data.get("phone"))
        button2 = browser.find_element(By.XPATH, '//*[@id="s2id_lead_project_ids"]/a/span[2]')
        button2.click()
        project = browser.find_element(By.XPATH, '/html/body/div[4]/div/input')
        project.send_keys(subproject)
        project.send_keys(Keys.RETURN)


        # browser.save_screenshot(save_path[0])
        save = browser.find_element(By.XPATH, '//*[@id="new_lead"]/div[6]/input')
        save.click()

        browser.implicitly_wait(5)
        
        # browser.save_screenshot(save_path[1])
        browser.close()
        browserLog.info("dra executed successfully")
        return 1

    except Exception as e:
        print(str(e))
        browserLog.exception("dra error occured ")
        # browser.save_screenshot(save_path[2])
        return -1

subproject="Centralia"
path="."
dra(subproject, browser, site_data, lead_data, path)