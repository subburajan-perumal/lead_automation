from data import all_sites
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from data import constants
from selenium.webdriver.common.alert import Alert


print("Present..")

akshaya = {
        "url": "https://www.tvsemerald.com/lp/cp/?srd=5d08ad2d5e3c3009976bffa9",
        "email": "",
        "pass": "",
        "cpname": "Lead Automation",
        "cpphn": "9000000000",
        "key_words": ["TVS Emerald Flourish", "TVS Emerald GreenAcres Apts", "TVS Emerald Green Enclave", 
        "TVS Emerald LightHouse", "TVS Emerald Peninsula", "TVS Emerald Hamlet", "tvs-green-enclave.com", "Porur", "Green Enclave"],
        "active": 1
    }

engine = './geckodriver'

first_name = "Test"
last_name = "Test"
email1 = "redacted@example.com"
sub_project_name = 'TVS Emerald Flourish'
phone = '9000000000'
name1 = first_name + ' ' + last_name

try:
    s=Service(engine)
    browser=webdriver.Firefox(service=s)

    '''
    all_sites.sites[site_name]["url"]
    all_sites.sites[site_name]["email"]
    all_sites.sites[site_name]["pass"]
    '''

    browser.get(akshaya["url"])
    client_name=browser.find_element(By.XPATH,'/html/body/div/div/div/div/div/div/div/form/div[2]/div/div/input[1]')
    client_name.send_keys(name1)
    client_email=browser.find_element(By.XPATH,'/html/body/div/div/div/div/div/div/div/form/div[3]/div/div/input')
    client_email.send_keys(email1)
    client_phone=browser.find_element(By.XPATH,'//html/body/div/div/div/div/div/div/div/form/div[4]/div/div/div/input')
    client_phone.send_keys(phone)
    project=Select(browser.find_element(By.XPATH,'/html/body/div/div/div/div/div/div/div/form/div[5]/div/div/select'))
    project.select_by_visible_text(sub_project_name)
    channel_name=browser.find_element(By.XPATH,'/html/body/div/div/div/div/div/div/div/form/div[6]/div/div/input')
    channel_name.send_keys(akshaya["cpname"])
    channel_phone=browser.find_element(By.XPATH,'/html/body/div/div/div/div/div/div/div/form/div[7]/div/div/input')
    channel_phone.send_keys(akshaya["cpphn"])
    comment=browser.find_element(By.XPATH,'/html/body/div/div/div/div/div/div/div/form/div[8]/div/div/textarea')
    comment.send_keys('Nil')

    #browser.save_screenshot(save_path1)    
    #upload_an_attachment(lead_id, save_path1)

    submit = browser.find_element(By.XPATH, '/html/body/div/div/div/div/div/div/div/form/div[9]/div/div/input')
    submit.click()
    time.sleep(4)

    alert = Alert(browser)
    #print(alert.text)
    alert.accept()

    time.sleep(5)
    #browser.save_screenshot(save_path)
    browser.quit()
    #upload_an_attachment(lead_id, save_path)

    time.sleep(5)    
    browser.quit()

except Exception as e:
    print("Exception...")
    print(e)
    time.sleep(5)    
    browser.quit()
