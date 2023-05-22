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
  "email": "LeadAutomation",
  "name": "urban_tree",
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
  "url": "https://utcrm.net/index.php"
}
lead_data = {
    "lead_id":"L000001",
    "name":"firstname",
    "first_name":"testfirstname",
    "last_name":"testlastname",
    "email" :"redacted@example.com",
    "phone" :"9000000000",
    "project_enquired_for" :"Silver Fields Phase II",
    "interested_properties":"",
    "interested_localities" : ""
}
def urban_tree(subproject, browser, site_data, lead_data, path):
    try:
        browser.get(site_data["url"])
        phone_no= PN.parse(lead_data['phone'])
        phone_national_number=phone_no.national_number
        phone_country_code=phone_no.country_code

        time.sleep(5)

        email=browser.find_element(By.XPATH,'//*[@id="username"]')
        email.send_keys(site_data["email"])
        time.sleep(1)

        pwdd=browser.find_element(By.XPATH,'//*[@id="password"]')
        pwdd.send_keys(site_data["pass"])

        submit = browser.find_element(By.XPATH,'/html/body/div[2]/div[2]/div[1]/div/div/div/div/div[2]/div/div[1]/form/div[3]/div/button')
        submit.click()
        time.sleep(20)    

        browser.get("https://utcrm.net/index.php?module=Appointments&view=List")    
        time.sleep(10)

        add_enquiry=browser.find_element(By.XPATH,'//*[@id="Appointments_listView_basicAction_LBL_ADD_RECORD"]')
        add_enquiry.click()
        time.sleep(5)

        firstnamelead=browser.find_element(By.XPATH,'//*[@id="Appointments_editView_fieldName_contactname"]')
        firstnamelead.send_keys(lead_data['name'])
        time.sleep(1)

        lastnamelead=browser.find_element(By.XPATH,'//*[@id="Appointments_editView_fieldName_companyname"]')
        lastnamelead.send_keys(lead_data['name'])
        time.sleep(1)

        emaillead=browser.find_element(By.XPATH,'//*[@id="Appointments_editView_fieldName_email"]')
        emaillead.send_keys(lead_data['email'])
        time.sleep(1)

        phone_code=browser.find_element(By.XPATH,'/html/body/div[2]/div[3]/div/div[2]/div[2]/form/table[1]/tbody/tr[2]/td[2]/div/span/div[1]/a/span')
        phone_code.click()
        time.sleep(1)

        phone_code=browser.find_element(By.XPATH,'/html/body/div[2]/div[3]/div/div[2]/div[2]/form/table[1]/tbody/tr[2]/td[2]/div/span/div/div/div/input')
        phone_code.send_keys(str("+") + str(phone_country_code))  
        phone_code.send_keys(Keys.RETURN)

        contact=browser.find_element(By.XPATH,'//*[@id="Appointments_editView_fieldName_mobile"]')
        time.sleep(1)
        contact.send_keys(phone_national_number)
        contact.send_keys(Keys.RETURN)        
        time.sleep(1)

        project=browser.find_element(By.XPATH,'/html/body/div[2]/div[3]/div/div[2]/div[2]/form/table[1]/tbody/tr[4]/td[4]/div/span/div/a/span')
        project.click()
        time.sleep(1)

        project=browser.find_element(By.XPATH,'/html/body/div[2]/div[3]/div/div[2]/div[2]/form/table[1]/tbody/tr[4]/td[4]/div/span/div/div/div/input')
        project.send_keys(subproject)
        project.send_keys(Keys.RETURN)
        time.sleep(1)

        submitbutton = browser.find_element(By.XPATH,'/html/body/div[2]/div[3]/div/div[2]/div[2]/form/div[1]/span/button')
        submitbutton.click()

        time.sleep(10)

        return 1
    
    except Exception as e:
        print(str(e))
        return -1
        

subproject="Silver Fields Phase II"
path="./geckodriver.exe"
urban_tree(subproject, browser, site_data, lead_data, path)