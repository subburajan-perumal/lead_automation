
from sqlite3 import SQLITE_DROP_TABLE
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
     "name": "Test",
      "first_name": "Test",
    "last_name": "Test", 
    "email": "redacted@example.com", 
    "phone": "+19514882916",
     "project_enquired_for": "",
      "interested_properties": "SPR Market of India", 
      "interested_localities": "Perambur",
       "initial_enquiry_particulars_automation": ""
    }

ph_number=PN.parse(lead_data['phone'])
country_name = (GC.description_for_number(ph_number,"en"))

site_data={"_id":{"$oid":"623c25874dca8f32e924417b"},"name":"casagrand","url":"http://cp.sell.do/users/sign_in","email":"redacted@example.com","pass":"REDACTED","status":1,"project_list":[{"project_name":"CG Zenith","keywords":["Casagrand Zenith","Zenith"],"location":[]},{"project_name":"CG Esquire","keywords":["Casagrand Esquire"],"location":[]},{"project_name":"CG Tudor","keywords":["Casagrand Tudor","Brigade Bonito","Brigade Xanadu","Signature City"],"location":[]},{"project_name":"CG Savoye","keywords":["Casagrand Savoye","Godrej Azure","Radiance Sapphire","Olympia Opaline","TCP Altura"],"location":[]},{"project_name":"CG Supremus","keywords":["Casagrand Supremus"],"location":[]},{"project_name":"CG ECR 14","keywords":["Casagrand ECR 14"],"location":[]},{"project_name":"CG Crescendo Elite","keywords":["Casagrand Crescendo Elite"],"location":[]},{"project_name":"CG Crescendo Compact","keywords":["Casagrand Crescendo Compact"],"location":[]},{"project_name":"CG Millenia","keywords":["Casagrand Millenia"],"location":[]},{"project_name":"CG Royale","keywords":["Casagrand Royale"],"location":[]},{"project_name":"CG Utopia","keywords":["Casagrand Utopia","Peninsula"],"location":[]},{"project_name":"CG Athens","keywords":["Casagrand Athens"],"location":[]},{"project_name":"CG FirstCity","keywords":["Casagrand FirstCity"],"location":[]}]}

def getName(name):
    splited_name = name.split(" ")

    if len(splited_name) == 1:

        return splited_name[0], splited_name[0]
    elif len(splited_name) == 2:
        return splited_name[0], splited_name[1]
    elif len(splited_name) == 3:
        return splited_name[0]+splited_name[1], splited_name[2]
    else:
        return "" ""

def casagrand(subproject, browser, site_data, lead_data, automate_path):
    try:
        browserLog.info(f"Site: {site_data['name']}, Project:{subproject}")
        save_path = automate_path
        fullname=str(lead_data['name'])
        first_name,last_name=getName(fullname)
        browser.get(site_data["url"])
        fl_email = browser.find_element(By.ID, "user_email")
        fl_email.send_keys(site_data["email"])
        fl_password = browser.find_element(By.ID,"user_password")
        fl_password.send_keys(site_data["pass"])
        browser.find_element(By.XPATH,'//*[@id="new_user"]/div[4]/div[2]/button').click()
        time.sleep(10)

        Leads = browser.find_element(By.XPATH, '/html/body/nav/div/ul[1]/li[2]/a')
        Leads.click()
        time.sleep(10)
        
        addlead = browser.find_element(By.XPATH, "/html/body/div/div/div[1]/div/ul/li/ul/li[2]/a")
        addlead.click()
        time.sleep(10)

        firstname = browser.find_element(By.ID, "lead_first_name")
        firstname.send_keys(fullname)
        lastname = browser.find_element(By.ID, "lead_last_name")
        lastname.send_keys(fullname)

        #nri = browser.find_element(By.ID, "lead_nri")
        #nri.click()
        #nri.click()

        f_mail = browser.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/form/div[2]/div[2]/div[2]/div[1]/div/div/a')
        f_mail.click()
        time.sleep(2)
        f_alt_mail = browser.find_element(By.XPATH, '/html/body/div[3]/div/input')
        f_alt_mail.click()
        time.sleep(2)
        f_alt_mail.send_keys(lead_data['email'])
        f_alt_mail.send_keys(Keys.RETURN)
        f_phone = browser.find_element(By.XPATH, '//*[@id="lead_phone"]')
        f_phone.click()
        time.sleep(2)
        f_phone.send_keys(lead_data['phone'])
        button2 = browser.find_element(By.XPATH, '//*[@id="s2id_lead_project_ids"]/a/span[2]')
        button2.click()
        time.sleep(2)
        f_project = browser.find_element(By.XPATH, '/html/body/div[4]/div/input')
        f_project.send_keys(subproject)
        f_project.send_keys(Keys.RETURN)

        country = browser.find_element(By.XPATH, '//*[@id="lead_country"]')
        country.send_keys(country_name)
    
       # browser.save_screenshot(save_path[0])      

        fs_save = browser.find_element(By.XPATH, '//*[@id="new_lead"]/div[6]/input')
        fs_save.click()
        time.sleep(10)
        
        # browser.save_screenshot(save_path[1])
        # browser.close()
        return 1
    except Exception as e:
        browserLog.exception(f"Site:{site_data['name']}")
        # browser.save_screenshot(save_path[2])
        return -1


subproject="CG Tudor"
path="."
casagrand(subproject, browser, site_data, lead_data, path)