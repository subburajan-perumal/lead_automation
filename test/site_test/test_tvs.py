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


site_data = {"_id": {"$oid": "623c25874dca8f32e924418a"}, 
"name": "tvs",
 "url": "https://cp.tvsemerald.com/users/sign_in", 
 "email": "redacted@example.com", 
 "pass": "REDACTED",
  "cpname": "Lead Automation", 
  "cpphn": "9000000000", "status": 1,
   "project_list":
    [{"project_name": "TVS Emerald Green Hills", "keywords": ["Lumina", "TVS Emerald Green Acres", "GreenAcres", "Shriram Joy", "Park 63", "Shriram Park", "Shriram Shankari", "Lancor Lumina"], "location":[], "projectStatus":1}, {"project_name": "TVS Emerald Green Enclave", "keywords": ["TVS Emerald Green Enclave", "Porur", "None (default)", "Green Enclave"], "location":["Porur"], "projectStatus":1}, {"project_name": "TVS Emerald LightHouse", "keywords": [
    "LightHouse", "Alliance Galleria", "Light House", "Tuxedo", "Radiance The Pride", "Elevate 21", "TVS Emerald LightHouse"], "location":[], "projectStatus":1}, {"project_name": "TVS Emerald Manapakkam", "keywords": [], "location":[], "projectStatus":1}, {"project_name": "TVS Emerald Hamlet", "keywords": ["Emerald Hamlet", "Adityaram", "Sobha Gardenia", "Amethyst", "House of Hiranandani", "Silver Springs", "Tango", "TCP Altura"], "location":[], "projectStatus":1}], "url2": "https://cp.tvsemerald.com/admin/leads?locale=en", "site_data": {"username": "redacted@example.com", "password": "REDACTED", "channel_partnername": "Lead Automation", "phone_no": "9000000000"}}
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
def tvs(subproject, browser, site_data, lead_data, path):
    try:
        browser.get(site_data["url"])
        phone_no= PN.parse(lead_data['phone'])
    
        #search=browser.find_element(By.XPATH,'/html/body/div[2]/div/div[2]/section/div[1]/div/div[2]/div/form/fieldset[1]/input')
        search=browser.find_element(By.XPATH,'//*[@id="user_login"]')        
        search.send_keys(site_data["email"])
        #time.sleep(3)
        
        #name  = browser.find_element(By.NAME, "Pname")
        #name.send_keys(name1)        
        
        time.sleep(1)
        pwdd=browser.find_element(By.XPATH,'//*[@id="user_password"]')
        pwdd.send_keys(site_data["pass"])
        
        #passo=browser.find_element(By.XPATH,'/html/body/div[1]/div[1]/div/div/div[2]/div[3]/form/input[1]')
        #passo.send_keys(all_sites.sites[site_name]["pass"])
        time.sleep(1)        
        submit=browser.find_element(By.XPATH,'/html/body/section/div/div/div[1]/div/form[2]/div[4]/input')
        submit.send_keys(Keys.RETURN)

        time.sleep(6)
        #open new tab
        #browser.find_element(By.TAG_NAME,'body').send_keys(Keys.COMMAND + 't')
        browser.get(site_data["url2"])

        time.sleep(3)
        addlead=browser.find_element(By.XPATH,'/html/body/div[1]/section/div/div/div[2]/div/a')
        addlead.send_keys(Keys.RETURN)
        time.sleep(3)
        
        firstnamelead=browser.find_element(By.XPATH,'//*[@id="lead_first_name"]')
        firstnamelead.send_keys(lead_data['name'])
        time.sleep(1)

        lastnamelead=browser.find_element(By.XPATH,'//*[@id="lead_last_name"]')
        lastnamelead.send_keys(lead_data['name'])
        time.sleep(1)

        # emaillead=browser.find_element(By.XPATH,'//*[@id="lead_email"]')
        # emaillead.send_keys(lead_data['email'])
        # time.sleep(1)                

        #projectlead=browser.find_element(By.XPATH,'/html/body/div[3]/div[2]/div/div[2]/div/div/c-related-source-data-table-lwc/c-create-new-lead/section/div/div/div/div[1]/div[2]/div/div/lightning-combobox/div[1]/lightning-base-combobox/div/div[1]/button')
        #projectlead=Select(browser.find_element(By.ID,'combobox-button-618'))
        #projectlead.select_by_visible_text("Radiance Maraikayar Manor")        
        #time.sleep(5) 

        #projectlead2=browser.find_element_by_xpath('/html/body/div[3]/div[2]/div/div[2]/div/div/c-related-source-data-table-lwc/c-create-new-lead/section/div/div/div/div[1]/div[2]/div/div/lightning-combobox/div/lightning-base-combobox/div/div[1]/button/span/text()')
	#/html/body/div[3]/div[2]/div/div[2]/div/div/c-related-source-data-table-lwc/c-create-new-lead/section/div/div/div/div[1]/div[2]/div/div/lightning-combobox/div/lightning-base-combobox/div/div[1]/button
        #projectlead2=browser.find_element_by_data-value(sub_project_name)    
        #projectlead2.click()            
        #time.sleep(5)       

        #namelead=browser.find_element(By.XPATH,'/html/body/div[3]/div[2]/div/div[2]/div/div/c-related-source-data-table-lwc/c-create-new-lead/section/div/div/div/div[1]/div[1]/div/div/div/input')
        #namelead.send_keys(name1)
        #time.sleep(1)

        #namelead=browser.find_element(By.XPATH,'/html/body/div[3]/div[2]/div/div[2]/div/div/c-related-source-data-table-lwc/c-create-new-lead/section/div/div/div/div[1]/div[1]/div/div/div/input')
        #namelead.send_keys(name1)
        #time.sleep(1)

        ## COUNTRY        
        #country2 = browser.find_element(By.XPATH, '/html/body/div[3]/div[2]/div/div[2]/div/div/c-related-source-data-table-lwc/c-create-new-lead/section/div/div/div/div[2]/div[2]/div[1]/div/lightning-combobox/div/lightning-base-combobox/div/div[1]/button')
        #country2.click()
        #time.sleep(1)        
        #country2.send_keys(country_name)
        #time.sleep(1)        
        #country2.send_keys(Keys.RETURN)
        #time.sleep(1)

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
        
        #contact.send_keys(phone)
        time.sleep(1)

        projectlead=browser.find_element(By.XPATH,'/html/body/div[3]/form/div/div/div/div[2]/div/div[2]/div[2]/div[2]/div/div/div[1]')
        #projectlead=browser.find_element_by_xpath('/html/body/div[3]/form/div/div/div/div[2]/div/div[2]/div[4]/div/div/div/div[1]/div')        
        #time.sleep(5)        
        projectlead.click()
        #projectlead.send_keys("E")                
        #time.sleep(2) 
        #projectlead.send_keys(Keys.DOWN)        
        #projectlead.send_keys(sub_project_name)        
        #time.sleep(1)
        
        #projectlead.send_keys("Hello")
        #Smart Homes @ Green Enclave
        projectlead=browser.find_element(By.ID,'lead_project_id-selectized')
        projectlead.send_keys(subproject)                
        #time.sleep(10)        
        #projectlead.send_keys(Keys.ENTER)
        projectlead.send_keys(Keys.RETURN)        
        time.sleep(1)

      
        
        submitbutton = browser.find_element(By.XPATH,'/html/body/div[3]/form/div/div/div/div[3]/input')
        submitbutton.click()
        #browser.execute_script("arguments[0].click();", button)

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
        

subproject="TVS Emerald Aaranya"
# subproject="Villabelvedere/Eternity"
path="./geckodriver.exe"
tvs(subproject, browser, site_data, lead_data, path)