import site
from selenium.webdriver import Firefox
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support import expected_conditions as EC
from phonenumbers import geocoder as GC
import phonenumbers as PN
import time
import logging
logging.basicConfig(filename="execution.log",
    level=logging.INFO,
    format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s'
    )
browserLog=logging.getLogger("selenium_log")

# browserLog.setLevel=logging.INFO


driver="./geckodriver.exe"
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

site_data={"_id":{"$oid":"623c25874dca8f32e9244187"},"name":"radiance","url":"http://cp.radiancerealty.in/login.php","url2":"http://cp.radiancerealty.in/lead_add.php","email":"redacted@example.com","pass":"REDACTED","status":1,"project_list":[{"project_name":"Test Budigere","keywords":[],"location":[]},{"project_name":"Radiance Splendour","keywords":["Radiance Splendour"],"location":[]},{"project_name":"Radiance Blossom","keywords":["Radiance Blossom"],"location":[]},{"project_name":"Radiance Smartville","keywords":["Radiance Smartville","Adityaram"],"location":[]},{"project_name":"Radiance The Pride","keywords":["Radiance The Pride","Galleria","Pallavaram"],"location":["Pallavaram"]},{"project_name":"Radiance Suprema","keywords":["Radiance Suprema","Lokaa M","Voora Ocean","Vardaan","SPR High","Signature City"],"location":[]},{"project_name":"Radiance Sapphire","keywords":["Radiance Sapphire","Courtyards","Amethyst","Olympia Opaline","Risington","Savoye","Godrej Azure","Sholinganallur","Navalur","Siruseri","Kelambakkam","OMR"],"location":["Sholinganallur","Navalur","Siruseri","Kelambakkam","OMR"]}]}

def radiance(subproject, browser, site_data, lead_data, path):
    try:
        browserLog.info("radiance started")
        save_path= path
        phone_no= PN.parse(lead_data['phone'])
        country_name=GC.country_name_for_number(phone_no,'en')
        # country_code=phone_no.country_code
        fv_phoneNo=phone_no.national_number
        browser.get(site_data["url"])

        fl_username= browser.find_element(By.XPATH, '/html/body/div[2]/div/div[2]/section/div[1]/div/div[2]/div/form/fieldset[1]/input')
        fl_username.send_keys(site_data["email"])
        
        fl_password= browser.find_element(By.XPATH, '/html/body/div[2]/div/div[2]/section/div[1]/div/div[2]/div/form/fieldset[2]/input')
        fl_password.send_keys(site_data["pass"])
        fl_submit= browser.find_element(By.XPATH, '/html/body/div[2]/div/div[2]/section/div[1]/div/div[2]/div/form/div/button')
        fl_submit.send_keys(Keys.RETURN)

        time.sleep(1)
        #open new tab
        browser.find_element(By.TAG_NAME,'body').send_keys(Keys.COMMAND + 't')
        browser.get(site_data["url2"])
        
        time.sleep(2)
        f_name=browser.find_element(By.NAME, 'lname')
        f_name.send_keys(lead_data['name'])

        ## COUNTRY
        f_country = browser.find_element(By.XPATH, '//*[@id="select2-country-container"]')
        if str(f_country.text).lower()!=country_name.lower():
            print(country_name)
            f_country.click()
            f_country2 = browser.find_element(By.XPATH, '/html/body/div[4]/div/div[2]/section/div/div/div/form/div/div[2]/div[3]/span/span[1]/span/span[2]')
            f_country3= browser.find_element(By.XPATH,"/html/body/span/span/span[1]/input")
            f_country3.send_keys(country_name)
            f_selectcountry=browser.find_element(By.XPATH,'//li[contains(@id,"select2-country-result-")]')
            f_selectcountry.click()
            contact=browser.find_element(By.XPATH, '//*[@id="fmobileNo"]')
            
        else:
            contact=browser.find_element(By.XPATH, '//*[@id="mobileNo"]')
        
        contact.send_keys(fv_phoneNo)
        
        email= browser.find_element(By.ID, 'emailId')
        email.send_keys(lead_data['email'])
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
    
        project= browser.find_element(By.XPATH, '/html/body/div[4]/div/div[2]/section/div/div/div/form/div/div[8]/div[3]/span/span[1]/span/span[2]')
        project.click()
        search_project= browser.find_element(By.XPATH, '/html/body/span/span/span[1]/input')
        search_project.send_keys(subproject)
        # project_list= 
        project_list=browser.find_element(By.XPATH,'//li[contains(@id,"select2-interestedproject-" )]')
        project_list.click()
        
        # fs_button=browser.find_element(By.XPATH,'/html/body/div[4]/div/div[2]/section/div/div/div/form/div/center/button')
        
        try:
            fs_button=browser.find_element(By.XPATH,'/html/body/div[4]/div/div[2]/section/div/div/div/form/div/center/button')
            fs_button.click()    
        except StaleElementReferenceException as e:
            fs_button=browser.find_element(By.XPATH,'/html/body/div[4]/div/div[2]/section/div/div/div/form/div/center/button')
            fs_button.click()
           

        # browser.save_screenshot(save_path[0])
        browser.implicitly_wait(5)
        # browser.save_screenshot(save_path[1])
        browser.close()
        browserLog.info('radiance executed ')
        return 1

    except Exception as e:
        print(str(e))
        browserLog.error("radiance error occured")
        # browser.save_screenshot(save_path[2])
        return -1

subproject="Radiance Sapphire"
path="."
radiance(subproject, browser, site_data, lead_data, path)
