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
      "first_name": "",
    "last_name": "Manikandan", 
    "email": "redacted@example.com", 
    "phone": "9000000000",
     "project_enquired_for": "",
      "interested_properties": "SPR Market of India", 
      "interested_localities": "Perambur",
       "initial_enquiry_particulars_automation": ""
    }

site_data={"_id":{"$oid":"623c25874dca8f32e924418b"},"name":"vijayaraja","url":"https://vijayrajacrmsite.secure.force.com/channelpartnerleadform","partner_name":"Lead Automation","partner_email":"redacted@example.com","status":0,"project_list":[{"project_name":"VRX 360","keywords":["vrx","poonamall","Vijay Raja","Hiranandani Park","Shriram Divine","Kovur","Porur","poonamallee"],"location":["Kovur","Porur","poonamallee"]},{"project_name":"Exurb","keywords":[],"location":[]},{"project_name":"Classic","keywords":[],"location":[]},{"project_name":"Sanctuary","keywords":[],"location":[]}]}   
def vr(subproject, browser, site_data, lead_data, path):

    try:
        browser.get(site_data["url"])

        name  = browser.find_element(By.XPATH, '//*[@id="last_name"]')
        #name.send_keys(all_sites.sites[site_name]["partner"])
        name.send_keys(lead_data['name'])
        time.sleep(3)
        
        #name  = browser.find_element(By.XPATH, '/html/body/section[3]/div/div/div[2]/div/form/input[2]')
        #name.send_keys(name1)
        #intrest_project = browser.find_element(By.ID, 'leads_project')

        contact=browser.find_element(By.XPATH,'//*[@id="phone"]')
        contact.send_keys(lead_data['phone'])
        #time.sleep(3)

        email=browser.find_element(By.XPATH,'//*[@id="email"]')
        email.send_keys(lead_data['email'])
        #time.sleep(3)

        cpname  = browser.find_element(By.XPATH, '//*[@id="00N0o00000NVnu3"]')
        cpname.send_keys(site_data["partner_name"])
        #cpname.send_keys(partner_name)
        #time.sleep(3)

        cpemail=browser.find_element(By.XPATH,'//*[@id="00N0o00000OSmDr"]')
        cpemail.send_keys(site_data["partner_email"])
        time.sleep(3)
        
        #project=browser.find_element(By.XPATH,'/html/body/div/form/div/div[12]/div/select')
        project=Select(browser.find_element(By.XPATH,'/html/body/div/form/div/div[12]/div/select'))
        #project.send_keys(sub_project_name)
        project.select_by_visible_text(subproject)
        time.sleep(1)        


        #add=browser.find_element(By.XPATH,'/html/body/div/form/div/div[13]/div/button')
        add=browser.find_element(By.XPATH,'/html/body/div/form/div/div[13]/div/button')
        #add=browser.find_element(By.XPATH,'/html/body/section[3]/div/div/div[2]/div/form/input[6]')
        add.click()
        time.sleep(3)
        return 1
        # browser.save_screenshot(save_path)    
        # browser.quit()

        # upload_an_attachment(lead_id, save_path)
        
        # req = "Success"
        # lead = Lead(name=name1, props= sub_project_name, phone = phone, email = email1, status = req, created_at =  dt_string, attachments = save_path)
        # db.session.add(lead)
        # db.session.commit()
        # print('Successfully added' + str(lead.id) + ' ' + str(sub_project_name) + ' ' + str(lead.status))
    
    except Exception as e:
        print(str(e))
        return -1        

subproject="VRX 360"
path="."
vr(subproject, browser, site_data, lead_data, path)