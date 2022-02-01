from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from pymongo import MongoClient
import time
import os

def addlead(project,sub_project_name=None,**lead_data):
    #database
    print("akshaya")
    try:
        CONN=MongoClient("mongodb://REDACTED_MONGO_URI")
        DB = CONN['lead_automation']
        LEADS=DB['leads']
        SITE=DB['Site'].find_one({"name":project})
        print(SITE['name'])
        print("db working")
        
    except Exception as e:
        print("Error occured due to "+str(e))
    try:
        firefox_service=Service("/home/subburaj/LEAD_AUTOMATION/lead_automation/geckodriver")
        opt=Options()
        opt.headless=False
        browser=webdriver.Firefox(options=opt,service=firefox_service)
    except:
        print("browser not working")
    
    try:
        site_name = "akshaya"
        path = "./" + site_name
        fullname = lead_data['first_name'] + ' ' + lead_data['last_name']


        if sub_project_name == "Akshaya Tango":
            sub_project_name = 'Tango'
        if sub_project_name == "Akshaya Republic":
            sub_project_name = 'Republic'
        if sub_project_name == "Akshaya Today":
            sub_project_name = 'Today'
        if sub_project_name == "Akshaya OrlandO":
            sub_project_name = 'OrlandO'
        if sub_project_name == "Akshaya Earth":
            sub_project_name = 'Earth'
        if sub_project_name == "Akshaya Shanti":
            sub_project_name = 'Shanti'
        if sub_project_name == "Akshaya Poongavanam":
            sub_project_name = 'Poongavanam'
        if sub_project_name == "Thoraipakkam":
            sub_project_name = 'Tango'
        if sub_project_name == "Perungudi":
            sub_project_name = 'Tango'     
        if sub_project_name == "Pallavaram":
            sub_project_name = 'Tango'
        if sub_project_name == "OMR":
            sub_project_name = 'Today'
        if sub_project_name == "Kelambakkam":
            sub_project_name = 'Today'
        if sub_project_name == "Sholinganallur":
            sub_project_name = 'Tango'
        if sub_project_name == "Navalur":
            sub_project_name = 'Today'
    #browser# yield "on working"
        print("\tSelenium started")
        browser.get(SITE["url"])
        email = browser.find_element(By.ID, "user_email")
        email.send_keys(SITE["email"])
        password = browser.find_element(By.ID,"user_password")
        password.send_keys(SITE["pass"])
        browser.find_element(By.XPATH,"//button[@type='submit']").click()
        Leads = browser.find_element(By.LINK_TEXT, "Leads")
        Leads.click()
        addlead = browser.find_element(By.XPATH, "//a[@href='/broker/2150/leads/new']")
        addlead.click()
        firstname = browser.find_element(By.ID, "lead_first_name")
        firstname.send_keys(lead_data.get("first_name"))
        lastname = browser.find_element(By.ID, "lead_last_name")
        lastname.send_keys(lead_data.get("last_name"))
        mail = browser.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/form/div[2]/div[2]/div[2]/div[1]/div/div/a')
        mail.click()
        mail1 = browser.find_element(By.XPATH, '/html/body/div[3]/div/input')
        mail1.click()
        mail1.send_keys(lead_data.get("email"))
        mail1.send_keys(Keys.RETURN)
        phone1 = browser.find_element(By.XPATH, '//*[@id="lead_phone"]')
        phone1.click()
        phone1.send_keys(lead_data.get("phone"))
        button2 = browser.find_element(By.XPATH, '//*[@id="s2id_lead_project_ids"]/a/span[2]')
        button2.click()
        project1 = browser.find_element(By.XPATH, '/html/body/div[4]/div/input')
        project1.send_keys(sub_project_name)
        project1.send_keys(Keys.RETURN)
        
        time.sleep(5)
        browser.save_screenshot("./storage/test.png")
        browser.close()

        print("\tSelenium working properly")
        req="success"
    
    except:
        req="failed"
        print('error occured')
    
    finally:
        return req