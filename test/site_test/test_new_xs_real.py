from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.alert import Alert
import time

driver="geckodriver"
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

site_data={
  "_id": {
    "$oid": "62f08d9107113b8d462172c5"
  },
  "name": "xs",
  "url": "https://alamoxsreal.com/index.php/contact/?srd=6108f58eed23e9000000000c",
  "partner_email": "",
  "pass": "REDACTED",
  "partner_name": "Lead Automation",
  "status": 1,
  "project_list": [
    {
      "project_name": "XS Real- Magnus",
      "keywords": [
        "XS Real- Magnus"
      ],
      "projectStatus": 0
    },
    {
      "project_name": "XS Real Catalunya City",
      "keywords": [
        "XS Real Catalunya City",
        "OMR",
        "siruseri",
        "KG Earth Homes",
        "Pragnya Eden Park",
        "Kelambakam",
        "Navalur",
        "Padur",
        "Egattur",
        "Sholinganallur"
      ],
      "projectStatus": 1
    },
    {
      "project_name": "XS Real Courtyard",
      "keywords": [
        "XS Real Courtyard"
      ],
      "projectStatus": 0
    },
    {
      "project_name": "XS Real Skycity",
      "keywords": [
        "XS Real Skycity"
      ],
      "projectStatus": 0
    }
  ],
  "site_data": {},
  "days": 30
}  

def xs_new(subproject, browser, site_data, lead_data, path):

    try:
        # browserLog.info(f"Site: {site_data['name']}, Project:{subproject}")

        save_path=path
        browser.get(site_data["url"])
        time.sleep(5)

        name  = browser.find_element(By.XPATH, '//*[@id="main"]/div/div[2]/div/div/div/div[2]/div/div/div/div/div/div/div/div/form/div[2]/div/div/input')
        name.send_keys(lead_data['name'])
        time.sleep(3)
        
        contact=browser.find_element(By.XPATH,'//*[@id="main"]/div/div[2]/div/div/div/div[2]/div/div/div/div/div/div/div/div/form/div[3]/div/div/div/input')
        contact.send_keys(lead_data['phone'])

        email=browser.find_element(By.XPATH,'//*[@id="main"]/div/div[2]/div/div/div/div[2]/div/div/div/div/div/div/div/div/form/div[4]/div/div/input')
        email.send_keys(lead_data['email'])

        projectName = browser.find_element(By.XPATH, '//*[@id="main"]/div/div[2]/div/div/div/div[2]/div/div/div/div/div/div/div/div/form/div[5]/div/div/select')
        projectName.send_keys(subproject)
        projectName.send_keys(Keys.RETURN)

        cpName = browser.find_element(By.XPATH, '//*[@id="main"]/div/div[2]/div/div/div/div[2]/div/div/div/div/div/div/div/div/form/div[6]/div/div/input')
        cpName.send_keys(site_data["partner_name"])

        submitButton = browser.find_element(By.XPATH,'//*[@id="main"]/div/div[2]/div/div/div/div[2]/div/div/div/div/div/div/div/div/form/div[7]/div/div/input')
        submitButton.click()

        browser.save_screenshot(save_path[1])
                
        return 1
        
    
    except Exception as e:
        # browserLog.exception(f"Site:{site_data['name']}")
        browser.save_screenshot(save_path[2])

        return -1



subproject="XS Real- Magnus"
path="."
xs_new(subproject, browser, site_data, lead_data, path)