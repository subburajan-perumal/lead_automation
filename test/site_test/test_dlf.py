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

site_data={"_id":{"$oid":"623c25874dca8f32e924417c"},"name":"dlf","url":"https://cplr.dlf.in/index","url2":"https://cplr.dlf.in/addlead","email":"redacted@example.com","pass":"REDACTED","status":0,"project_list":[{"project_name":"DLF Parc Estate","keywords":["Adityaram","Radiance Smartville","Radiance Blossom","Radiance Sapphire","Courtyards","Amethyst","Sholinganallur","Navalur","Siruseri","Kelambakkam","OMR","Pudupakkam","Risington","Savoye","Godrej Azure","Olympia Opaline","Oragadam","Hirananandani Park","Alexandri","DLF Parc Estate","plot","villa","DLFTest"],"location":["Sholinganallur","Navalur","Siruseri","Kelambakkam","OMR","Pudupakkam"]}]}
    
def dlf(subproject, browser, site_data, lead_data, path):
    
    try:
        locationname="Siruseri"
        phone=PN.parse(lead_data['phone'])
        phoneno=phone.national_number
        countrycode="+"+str(phone.country_code)
        
        browser.get(site_data["url"])
        search=browser.find_element(By.XPATH,'/html/body/div/div/div/form/div[2]/input')        
        search.send_keys(site_data["email"])
        
        time.sleep(1)
        pwdd=browser.find_element(By.XPATH,'/html/body/div/div/div/form/div[3]/input')
        pwdd.send_keys(site_data["pass"])
        time.sleep(1)        
        submit=browser.find_element(By.XPATH,'/html/body/div/div/div/form/div[4]/button')
        submit.send_keys(Keys.RETURN)

        time.sleep(5)
        browser.get(site_data["url2"])

        
        
        namelead=browser.find_element(By.XPATH,'/html/body/div[2]/div/div/form/div[1]/div[1]/input')
        namelead.send_keys(lead_data['name'])
        time.sleep(1)

        projectlocation=browser.find_element(By.XPATH,'//*[@id="location"]')
        projectlocation.send_keys(locationname)        
        projectlocation.send_keys(Keys.RETURN)


        emaillead=browser.find_element(By.XPATH,'//*[@id="email"]')
        emaillead.send_keys(lead_data['email'])
        time.sleep(1)        


        remarks=browser.find_element(By.XPATH,'//*[@id="remarks"]')
        remarks.send_keys(subproject)
        time.sleep(1)

        country2 = browser.find_element(By.XPATH, '//*[@id="country_code"]')
        country2.click()
        time.sleep(1)        
        country2.send_keys(countrycode)
        time.sleep(1)        
        country2.send_keys(Keys.RETURN)
        time.sleep(1)

        contact=browser.find_element(By.XPATH,'/html/body/div[2]/div/div/form/div[2]/div[2]/input')
        contact.send_keys(phoneno)
        time.sleep(1)


        
        submitbutton = browser.find_element(By.XPATH,'//*[@id="submit"]')
        submitbutton.click()

        time.sleep(2)

        browser.close()
        return 1        
    
    except Exception as e:
        print(str(e))
        return -1

subproject="DLF Parc Estate"
path="."
dlf(subproject, browser, site_data, lead_data, path)
