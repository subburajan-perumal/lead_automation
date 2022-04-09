from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.alert import Alert
# from ..app.util.utility import getName
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

site_data={"_id":{"$oid":"623c25874dca8f32e9244184"},
"name":"lancor","url":"http://cp.sell.do/users/sign_in",
"email":"redacted@example.com","pass":"REDACTED","status":0,"project_list":[{"project_name":"Lancor Lumina","keywords":["GreenAcres","Green Acres","Shriram Joy","Park 63","Lumina","Guduvan","Shriram Park","Shriram Shankari","Shriram Joy","Shriram Lakeside","Perungalathur","LancorTest"],"location":["Perungalathur"]},{"project_name":"Lancor TCP Altura","keywords":["Courtyards","Risington","Brigade Residences","Thoraipakkam","Perungudi","Sholinganallur","House of Hiranandani","Akshaya OrlandO","Akshaya Tango","Akshaya Today","Casagrand Esquire","Risland","Savoye","Radiance Sapphire","Amethyst","House of Hiranandani","PBEL","Godrej Azure","Olympia Opaline","TCP Altura","Elevate 21","Anchorage","Mandarin","OMR","Kelambakkam","Sholinganallur","Navalur"],"location":["OMR","Kelambakkam","Sholinganallur","Navalur"]},{"project_name":"Lancor Infinys - Keelkattalai","keywords":["Galleria","Courtyards","Risington","Brigade Residences","Gardenia","Tuxedo","Peninsula","Akshaya Republic","Akshaya Earth","Akshaya Poongavanam","Tuxedo","Green Enclave","LighHouse","Light House","Winchester","Radiance The Pride","Pallavaram","Thoraipakkam","Perungudi"],"location":["Pallavaram","Thoraipakkam","Perungudi"]}]}
def lancor(subproject, browser, site_data, lead_data, path):
    try:
        first_name,last_name= lead_data['last_name'],lead_data['last_name']
        browser.get(site_data["url"])
        email = browser.find_element(By.ID, "user_email")
        email.send_keys(site_data["email"])
        password = browser.find_element(By.ID,"user_password")
        password.send_keys(site_data["pass"])
        browser.find_element(By.XPATH,"//button[@type='submit']").click()

        Leads = browser.find_element(By.LINK_TEXT, "Leads")
        Leads.click()
        addlead = browser.find_element(By.XPATH, "//a[@href='/broker/1893/leads/new']")
        addlead.click()

        firstname = browser.find_element(By.ID, "lead_first_name")
        firstname.send_keys(first_name)
        lastname = browser.find_element(By.ID, "lead_last_name")
        lastname.send_keys(last_name)

        #nri = browser.find_element(By.ID, "lead_nri")
        #nri.click()
        #nri.click()

        mail = browser.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/form/div[2]/div[2]/div[2]/div[1]/div/div/a')
        mail.click()
        mail1 = browser.find_element(By.XPATH, '/html/body/div[3]/div/input')
        mail1.click()
        mail1.send_keys(lead_data['email'])
        mail1.send_keys(Keys.RETURN)
        phone1 = browser.find_element(By.XPATH, '//*[@id="lead_phone"]')
        phone1.click()
        phone1.send_keys(lead_data['phone'])
        button2 = browser.find_element(By.XPATH, '//*[@id="s2id_lead_project_ids"]/a/span[2]')
        button2.click()
        project = browser.find_element(By.XPATH, '/html/body/div[4]/div/input')
        project.send_keys(subproject)
        project.send_keys(Keys.RETURN)

    # ?    upload_an_attachment(lead_id, save_path1)

        save = browser.find_element(By.XPATH, '//*[@id="new_lead"]/div[6]/input')
        save.click()
        
        time.sleep(5)
        # browser.save_screenshot(save_path) 
        # browser.quit()        
        # upload_an_attachment(lead_id, save_path)

        return 1

    except Exception as e:
        print(str(e))
        # browser.save_screenshot(save_path2)
        return -1
subproject="lancor lumina"
path="."
lancor(subproject, browser, site_data, lead_data, path)
