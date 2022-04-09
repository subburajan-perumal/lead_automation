
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
      "first_name": "subbu",
    "last_name": "Manikandan", 
    "email": "redacted@example.com", 
    "phone": "9000000000",
     "project_enquired_for": "",
      "interested_properties": "SPR Market of India", 
      "interested_localities": "Perambur",
       "initial_enquiry_particulars_automation": ""
    }
site_data={"_id":{"$oid":"623c25874dca8f32e924417a"},"name":"brigade","url":"https://form.jotform.com/202941029236047","email":"redacted@example.com","pass":"REDACTED","company":"Elite Lifespaces","agentf1":"Elite","agentl1":"Lifespaces","aph1":"9","aph2":"1","aph3":"9000000000","status":1,"project_list":[{"project_name":"Brigade Xanadu","keywords":["Brigade Xanadu","None (default)","Fomra Hues","Emerald Peninsula","Brigade Bonito","brigade-","Tudor","Signature City"],"location":[]},{"project_name":"WTC Residences Chennai","keywords":["Brigade Residences at WTC","Brigade Residences","Highliving","ARC The Palm"],"location":[]}]}
#working
def brigade(subproject:str, browser: Firefox, site_data:dict, lead_data:dict,automate_path:list):         
    try:    
        browserLog.info("brigade started")
        save_path = automate_path
        fullname= str(lead_data['name'])
        #need to change
        # first_name, last_name = getName(fullname)
        first_name=lead_data['first_name']
        last_name=lead_data['last_name']

    #browser# yield "on working"
        save_path= automate_path
        browser.get(site_data["url"])
        company_name = browser.find_element(By.XPATH, '//*[@id="input_5"]')
        company_name.send_keys(site_data["company"])
        #agent name
        f_agentf = browser.find_elements(By.XPATH, '//*[@id="first_6"]')
        f_agentf[0].send_keys(site_data["agentf1"])
        f_agentl = browser.find_elements(By.XPATH, '//*[@id="last_6"]')
        f_agentl[0].send_keys(site_data["agentl1"])
        
        #agent mobile number
        f_aph11 = browser.find_elements(By.XPATH, '//*[@id="input_7_country"]')
        f_aph11[0].send_keys(site_data["aph1"])
        f_aph21 = browser.find_elements(By.XPATH, '//*[@id="input_7_area"]')
        f_aph21[0].send_keys(site_data["aph2"])
        f_aph31 = browser.find_elements(By.XPATH, '//*[@id="input_7_phone"]')
        f_aph31[0].send_keys(site_data["aph3"])
        
        #agent email
        f_mail = browser.find_elements(By.XPATH, '//*[@id="input_8"]')
        f_mail[0].send_keys(site_data["email"])
        
        #client name
        f_firstname= browser.find_element(By.XPATH, '//*[@id="first_11"]')
        f_firstname.send_keys(first_name)
        f_lastname= browser.find_element(By.ID, 'last_11')
        f_lastname.send_keys(last_name)
        
        #mobile number 1
        f_aph1c = browser.find_element(By.XPATH, '//*[@id="input_12_country"]')
        f_aph1c.send_keys(site_data["aph1"])
        f_aph2c = browser.find_element(By.XPATH, '//*[@id="input_12_area"]')
        f_aph2c.send_keys(site_data["aph2"])
        f_aph3c = browser.find_element(By.XPATH, '//*[@id="input_12_phone"]')
        f_aph3c.send_keys(lead_data["phone"])
        
        #mobile number 2
        f_aph1c2 = browser.find_element(By.XPATH, '//*[@id="input_14_country"]')
        f_aph1c2.send_keys(site_data["aph1"])
        f_aph2c2 = browser.find_element(By.XPATH, '//*[@id="input_14_area"]')
        f_aph2c2.send_keys(site_data["aph2"])
        f_aph3c2 = browser.find_element(By.XPATH, '//*[@id="input_14_phone"]')
        f_aph3c2.send_keys(lead_data["phone"])
        
        #emails
        f_email11= browser.find_element(By.XPATH, '//*[@id="input_13"]')
        f_email11.send_keys(lead_data["email"])
        f_email21= browser.find_element(By.XPATH, '//*[@id="input_15"]')
        f_email21.send_keys(lead_data["email"])
        
        #project name
        project=Select(browser.find_element(By.XPATH, '//*[@id="input_16"]'))
        project.select_by_visible_text(subproject)

        # browser.save_screenshot(save_path[0])    

        # f_add=browser.find_element(By.XPATH,'//*[@id="input_2"]').click()
        browser.implicitly_wait(5)
        # time.sleep(10)
        # browser.save_screenshot(save_path[1])
        browser.close()
        browserLog.info("brigade executed successfully")
        print("brigage website work successfully")
        return 1

    except Exception as e:
        print(str(e))
        time(5)
        browserLog.error("brigade exception occured")
        # browser.save_screenshot(save_path[2])
    
        return -1

subproject="Brigade Xanadu"
path="."
brigade(subproject, browser, site_data, lead_data, path)
