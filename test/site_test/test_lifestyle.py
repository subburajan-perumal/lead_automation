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

# from app.tasks import lead

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

site_data={"_id":{"$oid":"623c25874dca8f32e9244185"},"name":"lifestyle","url":"https://lifestylehousing.co.in","email":"LeadAutomation","pass":"REDACTED","channel_partner":"LeadAutomation","status":1,"project_list":[{"project_name":"Lifestyle LeParadis","keywords":["Lifestyle LeParadis","Emerald Peninsula","Chlorophyll","Green Enclave","Utopia","Peninsula","None (default)","Signature City","Porur","LifestyleTest"],"location":["Porur"],"projectStatus":1},{"project_name":"Lifestyle Podium","keywords":["Lifestyle Podium","Podium","Appaswamy Clover By The River","Ceebros One 74","Goodwood","Olympia Good","Good Wood","Good wood","Alwarpet","T Nagar"],"location":["Alwarpet","T Nagar"],"projectStatus":1},{"project_name":"Lifestyle Vardaan","keywords":["Highliving","Voora Ocean","Vardaan","Radiance Suprema","SPR High"],"location":[],"projectStatus":1}],"site_data":{"url":"https://lifestylehousing.co.in","username":"LeadAutomation","password":"REDACTED","channel_partner":"LeadAutomation"}}
def lifetyle(subproject, browser, site_data, lead_data, path):
    phone=PN.parse(lead_data['phone'])
    

    phone_no = phone.national_number
    alternet_contact = phone.national_number
    whatsapp = phone.national_number
    remark = "NIL"
    project_intrested = subproject
    #flat_type = '1 BHK'
    enquiry_sourse = 'Channel Partner'
    enquiry_owner  = 'LeadAutomation'
    #location = 'A'
    #budget = 'Below 5'
    #enquiry_Medium = 'Server Call'
    #channel_partner = 'LeadAutomation'
    
    # save_paths = getsavePath(path, name1, phone, sub_project_name) 
    # save_path1 = save_paths[1]
    # save_path = save_paths[0]
    # save_path2 = save_paths[2]



    try:
        browser.get(site_data["url"])
        search=browser.find_element(By.ID,'username')
        search.send_keys(site_data["email"])
        passo=browser.find_element(By.ID,'password')
        passo.send_keys(site_data["pass"])
        submit=browser.find_element(By.CLASS_NAME,'signin-button').click()

        #submit.send_keys(Keys.RETURN)
        time.sleep(2)
        lead=browser.find_elements(By.ID,'menubar_item_Appointments')[1].click()
        time.sleep(2)

        adding=browser.find_element(By.CLASS_NAME,'icon-plus')
        adding.click()
        time.sleep(2)
        name  = browser.find_element(By.NAME, "contactname")
        name.send_keys(lead_data["name"])
        contact=browser.find_element(By.NAME,'mobile')
        contact.send_keys(phone_no)

        intrest_project = browser.find_element(By.XPATH, '/html/body/div[2]/div[3]/div/div[2]/div[2]/form/table[1]/tbody/tr[2]/td[2]/div/span/div/a/div/b')
        intrest_project.click()
        new = browser.find_element(By.XPATH, '/html/body/div[2]/div[3]/div/div[2]/div[2]/form/table[1]/tbody/tr[2]/td[2]/div/span/div/div/div/input')
        new.send_keys(project_intrested)
        new.send_keys(Keys.RETURN)

        intrest_project = browser.find_element(By.XPATH, '/html/body/div[2]/div[3]/div/div[2]/div[2]/form/table[1]/tbody/tr[2]/td[4]/div/span/div/a/div/b')
        intrest_project.click()
        new = browser.find_element(By.XPATH, '/html/body/div[2]/div[3]/div/div[2]/div[2]/form/table[1]/tbody/tr[2]/td[4]/div/span/div/div/div/input')
        new.send_keys(enquiry_owner)
        new.send_keys(Keys.RETURN)

        '''
        alt_contact = browser.find_element(By.NAME, 'altmobile')
        alt_contact.send_keys(alternet_contact)
        '''
        
        email=browser.find_element(By.NAME,'email')
        email.send_keys(lead_data["email"])

        '''
        whatsapp_contact = browser.find_element(By.NAME, 'whatsapp')
        whatsapp_contact.send_keys(whatsapp)
        '''

        intrest_project = browser.find_element(By.XPATH, '/html/body/div[2]/div[3]/div/div[2]/div[2]/form/table[1]/tbody/tr[4]/td[4]/div/span/div/a/div/b')
        intrest_project.click()

        '''
        new = browser.find_element(By.XPATH, '/html/body/div[2]/div[3]/div/div[2]/div[2]/form/table[1]/tbody/tr[4]/td[4]/div/span/div/div/div/input')
        new.send_keys(location)
        new.send_keys(Keys.RETURN)
        '''

        intrest_project = browser.find_element(By.XPATH, '/html/body/div[2]/div[3]/div/div[2]/div[2]/form/table[1]/tbody/tr[5]/td[2]/div/span/div/a/div/b')
        intrest_project.click()

        '''
        new = browser.find_element(By.XPATH, '/html/body/div[2]/div[3]/div/div[2]/div[2]/form/table[1]/tbody/tr[5]/td[2]/div/span/div/div/div/input')
        new.send_keys(flat_type)
        new.send_keys(Keys.RETURN)
        '''

        '''
        #Budget
        intrest_project = browser.find_element(By.XPATH, '/html/body/div[2]/div[3]/div/div[2]/div[2]/form/table[1]/tbody/tr[5]/td[4]/div/span/div/a/div/b')
        intrest_project.click()
        new = browser.find_element(By.XPATH, '/html/body/div[2]/div[3]/div/div[2]/div[2]/form/table[1]/tbody/tr[5]/td[4]/div/span/div/div/div/input')
        new.send_keys(budget)
        new.send_keys(Keys.RETURN)
        '''

        '''
        #Enqiry Souce
        intrest_project = browser.find_element(By.XPATH, '/html/body/div[2]/div[3]/div/div[2]/div[2]/form/table[1]/tbody/tr[6]/td[2]/div/span/div/a/div/b')
        intrest_project.click()
        new = browser.find_element(By.XPATH, '/html/body/div[2]/div[3]/div/div[2]/div[2]/form/table[1]/tbody/tr[6]/td[2]/div/span/div/div/div/input')
        new.send_keys(enquiry_sourse)
        new.send_keys(Keys.RETURN)

        #Enqiry Medium
        intrest_project = browser.find_element(By.XPATH, '/html/body/div[2]/div[3]/div/div[2]/div[2]/form/table[1]/tbody/tr[6]/td[4]/div/span/div/a/div/b')
        intrest_project.click()
        new = browser.find_element(By.XPATH, '/html/body/div[2]/div[3]/div/div[2]/div[2]/form/table[1]/tbody/tr[6]/td[4]/div/span/div/div/div/input')
        new.send_keys(enquiry_Medium)
        new.send_keys(Keys.RETURN)

        #Enqiry Status
        intrest_project = browser.find_element(By.XPATH, '/html/body/div[2]/div[3]/div/div[2]/div[2]/form/table[1]/tbody/tr[7]/td[2]/div/span/div/a/div/b')
        intrest_project.click()
        new = browser.find_element(By.XPATH, '/html/body/div[2]/div[3]/div/div[2]/div[2]/form/table[1]/tbody/tr[7]/td[2]/div/span/div/div/div/input')
        new.send_keys(enquiry_Medium)
        new.send_keys(Keys.RETURN)
        '''

        #Channel Partner
        intrest_project = browser.find_element(By.XPATH, '/html/body/div[2]/div[3]/div/div[2]/div[2]/form/table[1]/tbody/tr[7]/td[4]/div/span/div/a/div/b')
        intrest_project.click()
        new = browser.find_element(By.XPATH, '/html/body/div[2]/div[3]/div/div[2]/div[2]/form/table[1]/tbody/tr[7]/td[4]/div/span/div/div/div/input')
        new.send_keys(site_data["channel_partner"])
        new.send_keys(Keys.RETURN)

        #project=Select(browser.find_element(By.XPATH,'//*[@id="Appointments_editView_fieldName_description"]'))
        #project.select_by_visible_text(remark)
        
        
        # browser.save_screenshot(save_path1)    
        # upload_an_attachment(lead_id, save_path1)
        
        add=browser.find_element(By.XPATH,"/html/body/div[2]/div[3]/div/div[2]/div[2]/form/div[1]/span/button").click()
        time.sleep(7)

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
        # browser.save_screenshot(save_path2)
        # browser.quit()
        return -1
        # lead = Lead(name=name1, props=sub_project_name, phone=phone,
        #             email=email1, status=req, created_at=dt_string, attachments=save_path2)
        # db.session.add(lead)
        # db.session.commit()
        # print('Unknown Error' + str(lead.id) + ' ' +
            #   str(sub_project_name) + ' ' + str(lead.status))
        # send_mail(lead_id, save_path2, sub_project_name, name1)

        # upload_an_attachment(lead_id, save_path2)

subproject="Lifestyle LeParadis"
path="."
lifetyle(subproject, browser, site_data, lead_data, path)
