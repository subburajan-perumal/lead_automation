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
  "url": "https://cp.arunexcello.com/users/sign_in"
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
def arun_excello(subproject, browser, site_data, lead_data, path):
    try:
        browser.get(site_data["url"])
        phone_no= PN.parse(lead_data['phone'])
    
        search=browser.find_element(By.XPATH,'/html/body/header/nav/div/div/div[5]/div/a')        
        search.click()
        #time.sleep(3)       

        time.sleep(1)
        email=browser.find_element(By.XPATH,'//*[@id="user_login"]')
        email.send_keys(site_data["email"])

        time.sleep(1)
        pwdd=browser.find_element(By.XPATH,'//*[@id="user_password"]')
        pwdd.send_keys(site_data["pass"])
        
        time.sleep(1)        
        submit=browser.find_element(By.XPATH,'/html/body/section/div/div/div[1]/div/form[2]/div[4]/input')
        submit.send_keys(Keys.RETURN)

        time.sleep(10)

        browser.get("https://cp.arunexcello.com/admin/cp_lead_activities?locale=en")      

        time.sleep(3)
        addlead=browser.find_element(By.XPATH,'/html/body/div[1]/section/div/div[1]/div[2]/div/a')
        addlead.send_keys(Keys.RETURN)
        time.sleep(3)
        
        firstnamelead=browser.find_element(By.XPATH,'//*[@id="lead_first_name"]')
        firstnamelead.send_keys(lead_data['name'])
        time.sleep(1)

        lastnamelead=browser.find_element(By.XPATH,'//*[@id="lead_last_name"]')
        lastnamelead.send_keys(lead_data['name'])
        time.sleep(1)

        emaillead=browser.find_element(By.XPATH,'//*[@id="lead_email"]')
        emaillead.send_keys(lead_data['email'])
        time.sleep(1)                     

        contact=browser.find_element(By.XPATH,'//*[@id="lead_phone"]')
        time.sleep(1)        
        contact.click()        
        time.sleep(1)
        contact.send_keys(Keys.BACKSPACE)
        time.sleep(1)
        contact.send_keys(Keys.BACKSPACE)
        time.sleep(1)
        contact.send_keys(Keys.BACKSPACE)
        time.sleep(1)
        contact.send_keys(Keys.BACKSPACE)
        time.sleep(1)        
        contact.send_keys(lead_data['phone'])         
        time.sleep(1)

        project=Select(browser.find_element(By.ID,'lead_project_id'))
        project.select_by_visible_text(subproject)

        submitbutton = browser.find_element(By.XPATH,'/html/body/div[4]/form/div/div/div/div[2]/div[4]/input')
        submitbutton.click()

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
arun_excello(subproject, browser, site_data, lead_data, path)