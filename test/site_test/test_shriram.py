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
     "name": "testfirstname testlastname",
      "first_name": "testname",
    "last_name": "Manikandan", 
    "email": "redacted@example.com", 
    "phone": "9000000000",
     "project_enquired_for": "",
      "interested_properties": "SPR Market of India", 
      "interested_localities": "Perambur",
       "initial_enquiry_particulars_automation": ""
    }
site_data={"_id":{"$oid":"623c25874dca8f32e9244189"},"name":"shriram","url":"https://www.shriramproperties.com/synergy/","email":"redacted@example.com","pass":"","status":0,"mobile":"9000000000","channel_partner":"Lead Automation","project_list":[{"project_name":"Shriram Mangalam","keywords":["Divine City","Kovur","Porur","Mangadu","Vanagaram"],"location":["Kovur","Porur","Mangadu","Vanagaram"]},{"project_name":"Shriram Joy","keywords":["Shriram Joy","Lumina","GreenAcres","Green Acres"],"location":[]},{"project_name":"Shriram LR","keywords":["Shriram Shankari lakeside","Guduvancher","Shriram Shankari"],"location":[]},{"project_name":"Shriram One City","keywords":["Shriram One City"],"location":[]},{"project_name":"Shriram Park 63","keywords":["Shriram Park 63","Alliance Galleria","Park 63","Winchester","Shriramtest"],"location":[]}]}

def shriram(subproject, browser, site_data, lead_data, path):   
    try:
        browser.get(site_data["url"])
        phone=PN.parse(lead_data['phone'])
        phoneno=phone.national_number
    
        agree = browser.find_element(
            By.XPATH, '/html/body/div[1]/div[4]/div/div/div[3]/button').click()
        time.sleep(5)

        radiobox = browser.find_element(By.XPATH, '/html/body/div[1]/section[2]/div/article/div[2]/div/div/div[2]/div/div/div/form/div[1]/div/div[1]/div[1]/label')
        radiobox.click()
        partner = browser.find_element(
            By.XPATH, '/html/body/div[1]/section[2]/div/article/div[2]/div/div/div[2]/div/div/div/form/div[2]/div[1]/div/div[1]/span/span[1]/span/span[1]/span')
        partner.click()
        time.sleep(1)
        partner1 = browser.find_element(
            By.XPATH, '/html/body/span/span/span[1]/input')
        partner1.send_keys(site_data["channel_partner"])
        partner1.send_keys(Keys.RETURN)
        coustmer_name = browser.find_element(By.XPATH, '//*[@id="edit-customer-name"]')
        coustmer_name.send_keys(lead_data['name'])
        coustmer_email = browser.find_element(By.XPATH, '//*[@id="customers-email"]')
        coustmer_email.send_keys(lead_data['email'])
        code = Select(browser.find_element(By.XPATH, '//*[@id="edit-country-code"]'))
        code.select_by_visible_text('India (+91)')
        coustmer_phone = browser.find_element(By.XPATH, '//*[@id="phone"]')
        coustmer_phone.send_keys(phoneno)
        resident = Select(browser.find_element(
            By.XPATH, '//*[@id="edit-customer-residential-status"]'))
        resident.select_by_visible_text('Local')
        coustmer_city = browser.find_element(By.XPATH, '//*[@id="res_city"]')
        coustmer_city.send_keys('Chennai')
        project_city = Select(browser.find_element(
            By.XPATH, '//*[@id="uc_city"]'))
        project_city.select_by_visible_text('Chennai')
        time.sleep(3)
        area = Select(browser.find_element(By.XPATH, '//*[@id="input_9_16"]'))
        area.select_by_visible_text(subproject)
        comment = browser.find_element(By.XPATH, '//*[@id="input_9_12"]')
        comment.send_keys('Nil')
        email10 = browser.find_element(By.XPATH, '//*[@id="input_9_47"]')
        email10.send_keys(site_data["email"])
        phone10 = browser.find_element(By.XPATH, '//*[@id="input_9_48"]')
        phone10.send_keys(site_data["mobile"])
        
        
 
        
        submit = browser.find_element(
            By.XPATH, '//*[@id="gform_submit_button_9"]')
        submit.click()
        time.sleep(20)

        try:
            aa = WebDriverWait(browser, 5).until(
            EC.presence_of_element_located(
                (By.XPATH,"/html/body/div[3]/div/div/div[3]/button"))
                # (By.XPATH, "//*[@id='gform_9']/div[1]"))
            )
            aa.click()
            # end=browser.find_element(By.XPATH,"/html/body/div[3]/div/div/div[3]/button")
            # end.click()
        except Exception as e:
            print(str(e))
        return 1
       
    except Exception as e:
        print(str(e))
       
        
        return -1
subproject="Park 63"
path="."
shriram(subproject, browser, site_data, lead_data, path)