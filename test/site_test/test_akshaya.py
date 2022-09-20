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
site_data={"_id":{"$oid":"623c25874dca8f32e9244178"},"name":"akshaya","url":"http://cp.sell.do/users/sign_in","email":"redacted@example.com","pass":"REDACTED","status":1,"project_list":[{"project_name":"Tango","keywords":["Akshaya Tango","Alliance Galleria","Casagrand Esquire","Risland","Courtyards","Risington","Brigade Residences","Thoraipakkam","Perungudi","Sholinganallur","Pallavaram","House of Hiranandani","Gardenia","Tuxedo","Olympia Opaline","TCP Altura","Elevate 21","Anchorage","Mandarin","Alexandri","AkshayaTest"],"location":["Thoraipakkam","Perungudi","Sholinganallur","Pallavaram"]},{"project_name":"Republic","keywords":["Akshaya Re   public","Woodside","Green Enclave","Emerald Peninsula","Signature City"],"location":[]},{"project_name":"Today","keywords":["Akshaya Today","Savoye","Radiance Sapphire","PBEL","Godrej Azure","Kelambakkam","OMR","Navalur"],"location":["Kelambakkam","OMR","Navalur"]},{"project_name":"OrlandO","keywords":["Akshaya OrlandO"],"location":[]},{"project_name":"Earth","keywords":["Akshaya Earth"],"location":[]},{"project_name":"Shanti","keywords":["Akshaya Shanti"],"location":[]},{"project_name":"Poongavanam","keywords":["Akshaya Poongavanam"],"location":[]}]}

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



def akshaya(subproject:str, browser:Firefox, site_data:dict, lead_data:dict,automate_path:list):
    try:
        browserLog.info(f"Site: {site_data['name']}, Project:{subproject}")
        save_path = automate_path
        fullname=str(lead_data['name'])
        first_name,last_name=getName(fullname)
        browser.get(site_data["url"])
        fl_email = browser.find_element(By.ID, "user_email")
        fl_email.send_keys(site_data["email"])
        fl_password = browser.find_element(By.ID, "user_password")
        fl_password.send_keys(site_data["pass"])
        browser.find_element(By.XPATH, '//*[@id="new_user"]/div[4]/div[2]/button').click()
        time.sleep(10)
        # f_Leads = WebDriverWait(browser, 15).until(
        #     EC.presence_of_element_located((By.LINK_TEXT, "Leads")))
        f_Leads = WebDriverWait(browser, 15).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/nav/div/ul[1]/li[2]/a')))
        # f_Leads = browser.find_element(By.LINK_TEXT, "Leads")
        f_Leads.click()
        time.sleep(10)
        f_addlead = browser.find_element(
            By.XPATH, "//a[@href='/broker/2150/leads/new']")
        f_addlead.click()
        time.sleep(10)
        f_firstname = browser.find_element(By.ID, "lead_first_name")
        f_firstname.send_keys(first_name)
        f_lastname = browser.find_element(By.ID, "lead_last_name")
        f_lastname.send_keys(last_name)
        f_mail = browser.find_element(
                                    By.XPATH, 
                                    '/html/body/div[1]/div/div[2]/form/div[2]/div[2]/div[2]/div[1]/div/div/a'
                                    )
        f_mail.click()
        f_mail1 = browser.find_element(By.XPATH, '/html/body/div[3]/div/input')
        f_mail1.click()
        f_mail1.send_keys(lead_data.get("email"))
        f_mail1.send_keys(Keys.RETURN)
        f_phone = browser.find_element(By.XPATH, '//*[@id="lead_phone"]')
        f_phone.click()
        f_phone.send_keys(lead_data.get("phone"))
        f_button2 = browser.find_element(
            By.XPATH, '//*[@id="s2id_lead_project_ids"]/a/span[2]')
        f_button2.click()
        f_project1 = browser.find_element(
            By.XPATH, '/html/body/div[4]/div/input')
        f_project1.send_keys(subproject)
        f_project1.send_keys(Keys.RETURN)

        # browser.save_screenshot(save_path[0])
        f_save = browser.find_element(By.XPATH, '//*[@id="new_lead"]/div[6]/input')
        # f_save.click()
        browser.implicitly_wait(5)
        # browser.save_screenshot(save_path[1])
        browser.close()
        return 1

    except Exception as e:
        browserLog.exception(f"Site:{site_data['name']}")
        # print(str(e))
        # browser.save_screenshot(save_path[2])
        browser.close()
        return -1

subproject="Tango"
path="."
akshaya(subproject, browser, site_data, lead_data, path)