
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
site_data={"_id":{"$oid":"623c25874dca8f32e9244180"},"name":"gsquare","url":"https://cp.gsquarehousing.com","partner_name":"Lead Automation","status":0,"project_list":[{"project_name":"G Square Sands N Waves","keywords":["G Square Sands N Waves"],"location":[]},{"project_name":"G Square Sunnyvale","keywords":["G Square Sunnyvale"],"location":[]},{"project_name":"G Square Blue Breeze","keywords":["G Square Blue Breeze"],"location":[]},{"project_name":"G Square Seawoods","keywords":["G Square Seawoods"],"location":[]},{"project_name":"G Square Beach Walk","keywords":["G Square Beach Walk"],"location":[]}]}


def gsquare(subproject, browser, site_data, lead_data, path):
    try:
        browserLog.info("gsquare started")
        save_path=path

        browser.get(site_data["url"])
        name = browser.find_element_by_xpath('/html/body/div/div/div/form/div[2]/div/div/input')
        name.send_keys(lead_data['name'])
        mail = browser.find_element_by_xpath('/html/body/div/div/div/form/div[3]/div/div/input')
        mail.send_keys(lead_data['email'])
        phone1 = browser.find_element_by_xpath('/html/body/div/div/div/form/div[4]/div/div/div/input')
        phone1.click()
        phone1.send_keys(lead_data['phone'])
        minbudget = browser.find_element_by_xpath('/html/body/div/div/div/form/div[6]/div[1]/div/select')
        minbudget.click()
        minbudgetvalue = browser.find_element_by_xpath('/html/body/div/div/div/form/div[6]/div[1]/div/select/option[3]')
        minbudgetvalue.click()
        maxbudget = browser.find_element_by_xpath('/html/body/div/div/div/form/div[6]/div[2]/div/select')
        maxbudget.click()
        maxbudgetvalue = browser.find_element_by_xpath('/html/body/div/div/div/form/div[6]/div[2]/div/select/option[11]')
        maxbudgetvalue.click()
        channelpartnername = browser.find_element_by_xpath('/html/body/div/div/div/form/div[7]/div[1]/div/textarea')
        channelpartnername.get(site_data["partner_name"])

        # browser.save_screenshot(save_path[0])
        browser.implicitly_wait(5)
        # browser.save_screenshot(save_path[1])
        browser.close()
        browserLog.info("gsquare executed successfully")
        return 1

    except Exception as e:
        print(str(e))
        browserLog.log("gsquare Error occured")
        # browser.save_screenshot(save_path[2])
        return -1

subproject=""
path="."
gsquare(subproject, browser, site_data, lead_data, path)
