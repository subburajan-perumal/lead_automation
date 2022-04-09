import email
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

site_data={"_id":{"$oid":"623c25874dca8f32e9244188"},"name":"radiance_phase_2","url":"https://channelpartner.force.com","url2":"https://channelpartner.force.com/radiancerealtyChannel/s/leads","email":"redacted@example.com","pass":"REDACTED","status":0,"project_list":[{"project_name":"Radiance Elite","keywords":["Radiance Elite"],"location":[]},{"project_name":"Radiance Splendour","keywords":["Radiance Splendour"],"location":[]},{"project_name":"Radiance Smartville","keywords":["Radiance Smartville","Adityaram","Oragadam","Hirananandani Park"],"location":[]},{"project_name":"Radiance The Pride","keywords":["Pallavaram","Radiance The Pride","Galleria"],"location":[]},{"project_name":"Radiance Suprema","keywords":["Radiance Suprema","Lokaa M","Voora Ocean","Vardaan","SPR High","Signature City","Brigade Xanadu","Orchid Springs","RadianceTest"],"location":[]},{"project_name":"Radiance Blossom","keywords":["Radiance Blossom"],"location":[]},{"project_name":"Radiance Sapphire","keywords":["Radiance Sapphire","Courtyards","Amethyst","Sholinganallur","Navalur","Olympia Opaline","Siruseri","Kelambakkam","OMR","Risington","Savoye","Godrej Azure","Alexandri"],"location":[]},{"project_name":"Radiance Maraikayar Manor","keywords":["Radiance Maraikayar Manor"],"location":[]},{"project_name":"Radiance Prosper","keywords":[],"location":[]},{"project_name":"Radiance Residencia","keywords":[],"location":[]}]}    
def radiance_(subproject, browser, site_data, lead_data, path):
    
    try:
        phone=PN.parse(lead_data['phone'])
        phoneno=phone.national_number
        browser.get(site_data["url"])
        search=browser.find_element(By.XPATH,'/html/body/div[1]/div[1]/div/div/div[2]/div[3]/form/div[2]/div/input[1]')        
        search.send_keys(site_data["email"])
        time.sleep(1)
        pwdd=browser.find_element(By.XPATH,'//*[@id="password"]')
        pwdd.send_keys(site_data["pass"])
        submit=browser.find_element(By.XPATH,'/html/body/div[1]/div[1]/div/div/div[2]/div[3]/form/input[2]')
        submit.send_keys(Keys.RETURN)

        time.sleep(3)
        browser.get(site_data["url2"])

        time.sleep(3)
        newlead=browser.find_element(By.XPATH,'/html/body/div[3]/div[2]/div/div[2]/div/div/c-related-source-data-table-lwc/div[1]/div/div/div/div/div[3]/button[1]')
        newlead.send_keys(Keys.RETURN)
        time.sleep(3)
        
        namelead=browser.find_element(By.XPATH,'/html/body/div[3]/div[2]/div/div[2]/div/div/c-related-source-data-table-lwc/c-create-new-lead/section/div/div/div/div[1]/div[1]/div/div/input')
        namelead.send_keys(lead_data['name'])
        time.sleep(1)

        projectlead=browser.find_element_by_xpath('/html/body/div[3]/div[2]/div/div[2]/div/div/c-related-source-data-table-lwc/c-create-new-lead/section/div/div/div/div[1]/div[2]/div/lightning-combobox/div[1]/lightning-base-combobox/div/div[1]/button')
        projectlead.click()
        projectlead.send_keys(subproject)        
        projectlead.send_keys(Keys.RETURN)
        emaillead=browser.find_element(By.XPATH,'/html/body/div[3]/div[2]/div/div[2]/div/div/c-related-source-data-table-lwc/c-create-new-lead/section/div/div/div/div[2]/div[1]/div/div/lightning-input/div/input')
        emaillead.send_keys(lead_data['email'])
        time.sleep(1)        

        contact=browser.find_element(By.XPATH,'/html/body/div[3]/div[2]/div/div[2]/div/div/c-related-source-data-table-lwc/c-create-new-lead/section/div/div/div/div[2]/div[2]/div[2]/div/lightning-input/div/input')
        contact.send_keys(phoneno)
        time.sleep(1)

        commentsbox=browser.find_element(By.XPATH,'/html/body/div[3]/div[2]/div/div[2]/div/div/c-related-source-data-table-lwc/c-create-new-lead/section/div/div/div/div[4]/div/div/div/div/lightning-textarea/div/textarea')
        commentsbox.send_keys("None")
        time.sleep(1)
        submitbutton = browser.find_element(By.XPATH,'/html/body/div[3]/div[2]/div/div[2]/div/div/c-related-source-data-table-lwc/c-create-new-lead/section/div/footer/button[2]')
        submitbutton.click()

        time.sleep(3)
        return 1
    
    except Exception as e:
        print(str(e))
        return -1


subproject="Radiance Elite"
path="."
radiance_(subproject, browser, site_data, lead_data, path)