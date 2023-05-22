import phonenumbers
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



driver="./geckodriver.exe"
firefox_service = Service(driver)
opt = Options()
opt.add_argument ( "--incognito" )
browser = webdriver.Firefox ( 
                            options = opt ,
                            service = firefox_service,
                            # service_log_path=WEBDRIVER_LOG
                            )


site_data ={
  "_id": {
    "$oid": "63a27c4b5c473f2f74870218"
  },
  "days": 30,
  "email": "redacted@example.com",
  "name": "arun_excello",
  "pass": "REDACTED",
  "project_list": [
    {
      "project_name": "Four Greens - II",
      "keywords": [
        "Four Greens - II"
      ],
      "location": [],
      "projectStatus": 1
    }
  ],
  "status": 1,
  "partner": "9000000000",
  "url": "http://cp.edenpark.net/lead-cp-form.php"
}
lead_data = {
    "lead_id":"L000001",
    "name":"firstname",
    "first_name":"testfirstname",
    "last_name":"testlastname",
    "email" :"redacted@example.com",
    "phone" :"9000000000",
    "project_enquired_for" :"GreenA",
    "interested_properties":"",
    "interested_localities" : ""
}
def pragnya(subproject, browser, site_data, lead_data, path):
    try:

        browser.get(site_data["url"])
        browser.get(site_data["url"])
        phone_no= PN.parse(lead_data['phone'])
        phone_national_number=phone_no.national_number

        name  = browser.find_element(By.XPATH, '/html/body/div[2]/div/form/div[1]/div/input')
        name.send_keys(site_data['partner'])

        name  = browser.find_element(By.XPATH, '/html/body/div[2]/div/form/div[2]/div/input')
        name.send_keys(lead_data['name'])

        email=browser.find_element(By.XPATH,'/html/body/div[2]/div/form/div[3]/div/input')
        email.send_keys(lead_data['email'])

        contact=browser.find_element(By.XPATH,'/html/body/div[2]/div/form/div[4]/div/input')
        contact.send_keys(phone_national_number)

        try:
            block = browser.find_element(By.XPATH, '//*[@id="cn-accept-cookie"]')
            block.click()
        except:
            pass        

        add=browser.find_element(By.XPATH,'/html/body/div[2]/div/form/div[7]/div/button')
        add.click()

        time.sleep(10)

        # browser.save_screenshot(save_path)    
        # browser.quit()
        # upload_an_attachment(lead_id, save_path)
        
        return 1
        # lead = Lead(name=name1, props= sub_project_name, phone = phone, email = email1, status = req, created_at =  dt_string, attachments = save_path)
        # db.session.add(lead)
        # db.session.commit()
        # print('Successfully added' + str(lead.id) + ' ' + str(sub_project_name) + ' ' + str(lead.status))
    
    
    except Exception as e:
        print(str(e))
        return -1
        

subproject="Sindhuraa-Siruseri"
path="./geckodriver.exe"
pragnya(subproject, browser, site_data, lead_data, path)