import time
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
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.options import Options


# binary = FirefoxBinary('./geckodriver.exe')


save_path = ['./', './', './']

def sidharth(subproject:str,browser:Firefox,site_data:dict, lead_data:dict, path:list):

    try:
        # browserLog.info(f"Site: {site_data['name']}, Project:{subproject}")

        save_path=path
        browser.get(site_data["url"])
        time.sleep(30)

        browser.switch_to.frame('sandboxFrame')
        browser.switch_to.frame('userHtmlFrame')   
        browser.find_element(By.XPATH, '/html/body/div/div[2]/div/div/div[2]/div/div/a[2]/div/div[2]').click() 
        time.sleep(30)    

        browser.switch_to.frame('sandboxFrame')
        browser.switch_to.frame('userHtmlFrame')

        browser.find_element(By.XPATH, '//*[@id="loginName"]').send_keys(site_data['partner_name'])
        browser.find_element(By.XPATH, '//*[@id="passML"]').send_keys(site_data['pass'])
        browser.find_element(By.XPATH, '//*[@id="logingBtn"]').click()
        time.sleep(30)

        newLeadButton = browser.find_element(By.XPATH,'//*[@id="upladFile"]/div[1]/div[1]/div[1]/img')
        newLeadButton.click()
        time.sleep(10)

        name  = browser.find_element(By.XPATH, '//*[@id="addCName"]')
        name.click()
        time.sleep(10)
        name.send_keys(lead_data['name'])

        contact=browser.find_element(By.XPATH,'//*[@id="addCPh1"]')
        contact.click()
        time.sleep(10)
        contact.send_keys(lead_data['phone'])

        contact=browser.find_element(By.XPATH,'//*[@id="addCPh2"]')
        contact.click()
        time.sleep(10)
        contact.send_keys(lead_data['phone'])

        email=browser.find_element(By.XPATH,'//*[@id="addCMail1"]')
        email.click()
        time.sleep(10)
        email.send_keys(lead_data['email'])

        email=browser.find_element(By.XPATH,'//*[@id="addCMail2"]')
        email.click()
        time.sleep(10)
        email.send_keys(lead_data['email'])

        form=browser.find_element(By.XPATH, '//*[@id="addProject"]')
        form.click()
        time.sleep(10)
        form.send_keys(subproject)
        form.send_keys(Keys.RETURN)

        budget=browser.find_element(By.XPATH, '//*[@id="addBudget"]')
        budget.send_keys("80L - 100L")
        form.send_keys(Keys.RETURN)

        propType=browser.find_element(By.XPATH, '//*[@id="addType"]')
        propType.send_keys("3BHK")
        form.send_keys(Keys.RETURN)

        remarks=browser.find_element(By.XPATH, '//*[@id="addCRemark"]')
        remarks.click()
        time.sleep(10)
        remarks.send_keys("NIL")

        # browser.save_screenshot(save_path[0])

        submitButton = browser.find_element(By.XPATH,'//*[@id="addFileSubmit"]')
        submitButton.click()
        time.sleep(10)

        # browser.save_screenshot(save_path[1])
                
        return 1

    
    except Exception as e:
        # browserLog.exception(f"Site:{site_data['name']}")
        browser.save_screenshot(save_path[2])

        return -1


site_data = {
        "_id": {"$oid": "62f52d17dec044293f58dd9d"}, 
        "name": "sidharth",
        "url": "https://script.google.com/macros/s/AKfycbx-ICLnGQRawvV2hxiPItx1YwXH8R1gNPTIOH2oV2G4nQiW9KY_YfznguRDNa46wR5Fug/exec", 
        "email": "", 
        "pass": "REDACTED",
        "partner_name": "Lead Automation", 
        "status": 1,
        "project_list":
            [{"project_name": "Crown", "keywords": ["Sidharth", "Crown"],"projectStatus":1}, 
            {"project_name": "Sidharth", "keywords": ["Sidharth", "Northern star ", "Radiance Suprema", "Lokaa M One","KG Signature City ","Madhavaram"], "projectStatus":1}]
        }

lead_data = {
            "lead_id":"L000001",
            "name":"first_name lastname",
            "first_name":"testfirstname",
            "last_name":"testlastname",
            "email" :"redacted@example.com",
            "phone" :"9000000000",
            "project_enquired_for" :"GreenA",
            "interested_properties":"",
            "interested_localities" : ""
        }


subproject = 'Crown'
browser = webdriver.Firefox(executable_path='./geckodriver.exe')
result=sidharth("Crown", browser, site_data, lead_data, ".")
print(result)