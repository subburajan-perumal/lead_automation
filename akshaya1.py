from data import all_sites
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from data import constants


akshaya = {
        "url": "http://cp.sell.do/users/sign_in",
        "email": "redacted@example.com",
        "pass": "REDACTED",
        "key_words": ['Casagrand Zenith', 'Casagrand Esquire', 'Casagrand Tudor', 'Casagrand Savoye', 'Casagrand Supremus',
        'Casagrand Zenith', 'Casagrand ECR 14', 'Casagrand Primera', 'Casagrand Crescendo Elite', 'Casagrand Crecendo Compact',
        'Casagrand Millenia', 'Casagrand Royale', 'Casagrand Utopia', 'Casagrand Athens', 'Casagrand FirstCity'],
        "active": 0
    }

engine = './geckodriver'

first_name = "Test"
last_name = "Test"
email1 = "redacted@example.com"
sub_project_name = 'CG Zenith'
phone = '9000000000'



s=Service(engine)
browser=webdriver.Firefox(service=s)

'''
all_sites.sites[site_name]["url"]
all_sites.sites[site_name]["email"]
all_sites.sites[site_name]["pass"]
'''

browser.get(akshaya["url"])
email = browser.find_element(By.ID, "user_email")
email.send_keys(akshaya["email"])
password = browser.find_element(By.ID, "user_password")
password.send_keys(akshaya["pass"])
browser.find_element(By.XPATH, "//button[@type='submit']").click()
    

Leads = browser.find_element(By.LINK_TEXT, "Leads")
Leads.click()
addlead = browser.find_element(By.XPATH, "/html/body/div/div/div[1]/div/ul/li/ul/li[2]/a")
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
mail1.send_keys(email1)
mail1.send_keys(Keys.RETURN)
phone1 = browser.find_element(By.XPATH, '//*[@id="lead_phone"]')
phone1.click()
phone1.send_keys(phone)
button2 = browser.find_element(By.XPATH, '//*[@id="s2id_lead_project_ids"]/a/span[2]')
button2.click()
project = browser.find_element(By.XPATH, '/html/body/div[4]/div/input')
project.send_keys(sub_project_name)
project.send_keys(Keys.RETURN)
save = browser.find_element(By.XPATH, '//*[@id="new_lead"]/div[6]/input')
save.click()

time.sleep(5)    
browser.quit()


