from selenium.webdriver import Firefox
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
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


def hiranandani(subproject:str, browser:Firefox, site_data:dict, lead_data:dict,automate_path:list):
        ph_number=PN.parse(lead_data['phone'])
        phoneno=ph_number.national_number
        country_code = ph_number.country_code
        cc = str(country_code)
        try:
            browserLog.info(f"Site: {site_data['name']}, Project:{subproject}")
            save_path = automate_path
            fullname=str(lead_data['name'])
            first_name,last_name=getName(fullname)
            browser.get(site_data["url"])
            time.sleep(30)
            # browser.find_element(By.XPATH, '/html/body/button').click()
            browser.find_element(By.XPATH, '/html/body/div[3]/div[2]/div/div[1]/button/span').click()
            time.sleep(5)

            browser.find_element(By.XPATH, '/html/body/header/div/div[2]/div/nav/a[6]').click()
            time.sleep(5)

            country_code = Select(browser.find_element(By.XPATH,'//*[@id="cc"]'))
            country_code.select_by_value(cc)

            f_phone = browser.find_element(By.XPATH, '//*[@id="mobile"]')
            f_phone.click()
            f_phone.send_keys(phoneno)
            time.sleep(2)  

            f_mail = browser.find_element(By.XPATH, '/html/body/section[8]/div/div[2]/div/form/div[2]/div/input')
            f_mail.click()
            f_mail.send_keys(lead_data['email'])
            time.sleep(2)   


            browser.find_element(By.XPATH, '/html/body/button').click()
            browser.find_element(By.XPATH, '/html/body/div[5]/div/div/div[1]/button/span').click()

            time.sleep(5)

            browser.find_element(By.XPATH, '/html/body/button').click()
            browser.find_element(By.XPATH, '/html/body/div[5]/div/div/div[1]/button/span').click()


            f_name =  browser.find_element(By.XPATH, "/html/body/section[8]/div/div[2]/div/form/div[1]/div/input[1]")
            f_name.send_keys(lead_data['name'])
            time.sleep(10)

            # browser.save_screenshot(save_path[0])  
       
            fs_save = browser.find_element(By.XPATH, '/html/body/section[8]/div/div[2]/div/form/button')
            fs_save.click()
     

            # browser.save_screenshot(save_path[1])
            # browser.close()
            return 1

        except Exception as e:
            browserLog.exception(f"Site:{site_data['name']}")
            print(str(e))
            # browser.save_screenshot(save_path[2])
            # browser.close()
            return -1

lead_data={
    "lead_id": "920786000234230275",
     "name": "Manikandan",
      "first_name": "subbu",
    "last_name": "Manikandan", 
    "email": "redacted@example.com", 
    "phone": "+2554845211096",
     "project_enquired_for": "",
      "interested_properties": "SPR Market of India", 
      "interested_localities": "Perambur",
       "initial_enquiry_particulars_automation": ""
    }
site_data={"_id":{"$oid":"623c25874dca8f32e9244178"},
        "name":"hiranandani",
        "url":"https://hiranandanichennai.co.in/",
        "email":"redacted@example.com",
        "pass":"REDACTED","status":1,
        "project_list":[{"project_name":"Tango","keywords":["Akshaya Tango","Alliance Galleria","Casagrand Esquire","Risland","Courtyards","Risington","Brigade Residences","Thoraipakkam","Perungudi","Sholinganallur","Pallavaram","House of Hiranandani","Gardenia","Tuxedo","Olympia Opaline","TCP Altura","Elevate 21","Anchorage","Mandarin","Alexandri","AkshayaTest"],"location":["Thoraipakkam","Perungudi","Sholinganallur","Pallavaram"]},{"project_name":"Republic","keywords":["Akshaya Re   public","Woodside","Green Enclave","Emerald Peninsula","Signature City"],"location":[]},{"project_name":"Today","keywords":["Akshaya Today","Savoye","Radiance Sapphire","PBEL","Godrej Azure","Kelambakkam","OMR","Navalur"],"location":["Kelambakkam","OMR","Navalur"]},{"project_name":"OrlandO","keywords":["Akshaya OrlandO"],"location":[]},{"project_name":"Earth","keywords":["Akshaya Earth"],"location":[]},{"project_name":"Shanti","keywords":["Akshaya Shanti"],"location":[]},{"project_name":"Poongavanam","keywords":["Akshaya Poongavanam"],"location":[]}]
    }

# ph_number=PN.parse(lead_data['phone'])
# phoneno=ph_number.national_number
# country_code = ph_number.country_code
# print(country_code)
subproject="Tango"
path="."
hiranandani(subproject, browser, site_data, lead_data, path)
