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
from selenium.webdriver.common.action_chains import ActionChains



driver="./geckodriver.exe"
firefox_service = Service(driver)
opt = Options()
opt.add_argument ( "--incognito" )
browser = webdriver.Firefox ( 
                            options = opt ,
                            service = firefox_service,
                            # service_log_path=WEBDRIVER_LOG
                            )


site_data = {
        "_id": {"$oid": "62f52d17dec044293f58dd9d"}, 
        "name": "sidharth",
        "url": "https://nodal-time-327708.web.app/index.html", 
        "email": "", 
        "pass": "REDACTED",
        "partner_name": "Lead Automation", 
        "status": 1,
        "project_list":
            [{"project_name": "Crown", "keywords": ["Sidharth", "Crown"],"projectStatus":1}, 
            {"project_name": "Sidharth", "keywords": ["Sidharth", "Northern star ", "Radiance Suprema", "Lokaa M One","KG Signature City ","Madhavaram"], "projectStatus":1}]
        }

lead_data = {
            "lead_id":"L000001",
            "name":"first_name lastname",
            "first_name":"testfirstname",
            "last_name":"testlastname",
            "email" :"redacted@example.com",
            "phone" :"9000000000",
            "project_enquired_for" :"GreenA",
            "interested_properties":"",
            "interested_localities" : ""
        }

def sidharth(subproject, browser, site_data, lead_data, path):
    try:
        browser.get(site_data["url"])
        phone_no= PN.parse(lead_data['phone'])
    

        email=browser.find_element(By.XPATH,'//*[@id="loginName"]')
        email.send_keys(site_data["partner_name"])
        time.sleep(2)

        pwdd=browser.find_element(By.XPATH,'//*[@id="passML"]')
        pwdd.send_keys(site_data["pass"])
        time.sleep(2) 

        submit= browser.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div[2]/form[1]/div[4]')
        submit.click()
        time.sleep(10)    

        addlead=browser.find_element(By.XPATH,'/html/body/div[1]/div/div[1]/div/div[1]/div/div[2]/div/div/div/label[1]')
        addlead.click()
        time.sleep(3)
        
        name=browser.find_element(By.XPATH,'//*[@id="clientName_addLead"]')
        name.send_keys(lead_data['name'])
        time.sleep(1)

        emaillead=browser.find_element(By.XPATH,'//*[@id="mail1_addLead"]')
        emaillead.send_keys(lead_data['email'])
        time.sleep(1)                     

        contact=browser.find_element(By.XPATH,'//*[@id="ph1_addLead"]')       
        contact.send_keys(phone_no.national_number)         
        time.sleep(1)

        project=Select(browser.find_element(By.ID,'project_addLead'))
        project.select_by_visible_text(subproject)
        time.sleep(1)

        budget=Select(browser.find_element(By.ID,'budget_addLead'))
        budget.select_by_visible_text("20L - 40L")  
        time.sleep(1)

        type=Select(browser.find_element(By.ID,'type_addLead'))
        type.select_by_visible_text("4BHK") 
        time.sleep(1)       

        submitbutton = browser.find_element(By.XPATH,'/html/body/div[1]/div/div[2]/div/div[3]/button/span[1]/i')
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
        

subproject = 'Crown'
path="./geckodriver.exe"
sidharth(subproject, browser, site_data, lead_data, path)