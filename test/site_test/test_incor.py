from selenium import webdriver
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.alert import Alert
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

site_data={"_id":{"$oid":"623c25874dca8f32e9244182"},"name":"incor","url":"https://dashboard.reroot.in/business/login","url2":"https://dashboard.reroot.in/business/IncorGroup/quick-registration","email":"redacted@example.com","pass":"REDACTED","status":0,"project_list":[{"project_name":"PBEL City - Phase II","keywords":["House of Hiranandani","Amethyst","Courtyards","Sholinganallur","Siruseri","Risington","Eden Park","Olympia Opaline","TCP Altura","Elevate 21","Anchorage","Mandarin","Radiance Sap","Alexandri","INCOR","PBEL","INNCORTest"],"location":[]}]}
lead_data={
    "lead_id":"L000001",
    "name":"first_name lastname",
    "first_name":"testfirstname",
    "last_name":"testlastname",
    "email" :"redacted@example.com",
    "phone" :"9000000000",
    "project_enquired_for" :"Fomra Hues",
    "interested_properties":"",
    "interested_localities" : ""
}

def incor(subproject, browser, site_data, lead_data, path):
    try:
        browser.get(site_data["url"])
        time.sleep(3)
        #search=browser.find_element(By.XPATH,'/html/body/div[2]/div/div[2]/section/div[1]/div/div[2]/div/form/fieldset[1]/input')
        search=browser.find_element(By.XPATH,'/html/body/div/div[2]/div/div/div/div[2]/form/div/div[1]/input')        
        search.send_keys(site_data["email"])
        #time.sleep(3)
        
        #name  = browser.find_element(By.NAME, "Pname")
        #name.send_keys(name1)        
        
        time.sleep(1)
        pwdd=browser.find_element(By.XPATH,'//*[@id="password"]')
        pwdd.send_keys(site_data["pass"])
        
        #passo=browser.find_element(By.XPATH,'/html/body/div[1]/div[1]/div/div/div[2]/div[3]/form/input[1]')
        #passo.send_keys(all_sites.sites[site_name]["pass"])
        time.sleep(1)        
        submit=browser.find_element(By.XPATH,'/html/body/div/div[2]/div/div/div/div[2]/form/div/div[5]/button')
        submit.send_keys(Keys.RETURN)

        time.sleep(10)
        #open new tab
        #browser.find_element(By.TAG_NAME,'body').send_keys(Keys.COMMAND + 't')
        browser.get(site_data["url2"])

        time.sleep(3)
        #newlead=browser.find_element(By.XPATH,'/html/body/div[3]/div[2]/div/div[2]/div/div/c-related-source-data-table-lwc/div[1]/div/div/div/div/div[3]/button[1]')
        #newlead.send_keys(Keys.RETURN)
        #time.sleep(3)
        
        namelead=browser.find_element(By.XPATH,'/html/body/div[1]/div[3]/div[2]/div/div[1]/div[1]/div/div[3]/div[1]/input')
a        namelead.send_keys(lead_data['name'])
        time.sleep(1)

        #projectlead2=browser.find_element_by_xpath('/html/body/div[3]/div[2]/div/div[2]/div/div/c-related-source-data-table-lwc/c-create-new-lead/section/div/div/div/div[1]/div[2]/div/div/lightning-combobox/div/lightning-base-combobox/div/div[1]/button/span/text()')
	#/html/body/div[3]/div[2]/div/div[2]/div/div/c-related-source-data-table-lwc/c-create-new-lead/section/div/div/div/div[1]/div[2]/div/div/lightning-combobox/div/lightning-base-combobox/div/div[1]/button
        #projectlead2=browser.find_element_by_data-value(sub_project_name)    
        #projectlead2.click()            
        #time.sleep(5)       

        emaillead=browser.find_element(By.XPATH,'/html/body/div[1]/div[3]/div[2]/div/div[1]/div[1]/div/div[3]/div[2]/input')
        emaillead.send_keys(lead_data['email'])
        time.sleep(1)        

        #namelead=browser.find_element(By.XPATH,'/html/body/div[3]/div[2]/div/div[2]/div/div/c-related-source-data-table-lwc/c-create-new-lead/section/div/div/div/div[1]/div[1]/div/div/div/input')
        #namelead.send_keys(name1)
        #time.sleep(1)

        #namelead=browser.find_element(By.XPATH,'/html/body/div[3]/div[2]/div/div[2]/div/div/c-related-source-data-table-lwc/c-create-new-lead/section/div/div/div/div[1]/div[1]/div/div/div/input')
        #namelead.send_keys(name1)
        #time.sleep(1)

        ## COUNTRY        
        #country2 = browser.find_element(By.XPATH, '//*[@id="select2-chosen-123"]')
        #country2.click()
        #time.sleep(1)        
        #country2.send_keys(countrycode)
        #time.sleep(1)        
        #country2.send_keys(Keys.RETURN)
        #time.sleep(1)

        contact=browser.find_element(By.XPATH,'/html/body/div[1]/div[3]/div[2]/div/div[1]/div[1]/div/div[3]/div[3]/div[2]/input')
        contact.send_keys(lead_data['phone'])
        time.sleep(1)

        enquirysource=browser.find_element(By.XPATH,'/html/body/div[1]/div[3]/div[2]/div/div[1]/div[1]/div/div[3]/div[8]/div/a')        
        #enquirysource=browser.find_element(By.XPATH,'/html/body/div[9]/div/input')        
        time.sleep(1)
        enquirysource.click()
        #enquirysource2=browser.find_element(By.XPATH,'/html/body/div[9]/div/input')        
        #time.sleep(1)
        #enquirysource2.click()

        #time.sleep(1)        
        #enquirysource.send_keys(s2id_autogen131)
        #enquirysource.send_keys("Channel Partner - Lead Automation")
        enquirysource.send_keys("Lead Automation")        
        time.sleep(1)                
        #enquirysource.click()                
        enquirysource.send_keys(Keys.RETURN)
        time.sleep(1)
 
         #projectlead=browser.find_element(By.XPATH,'/html/body/div[3]/div[2]/div/div[2]/div/div/c-related-source-data-table-lwc/c-create-new-lead/section/div/div/div/div[1]/div[2]/div/div/lightning-combobox/div[1]/lightning-base-combobox/div/div[1]/button')
        #projectlead=Select(browser.find_element(By.ID,'combobox-button-618'))
        #projectlead=browser.find_element_by_xpath('/html/body/div[1]/div[3]/div[2]/div/div[1]/div[1]/div/div[3]/div[9]/div/ul/li[2]')
        #projectlead=browser.find_element_by_xpath('//*[@id="s2id_qregistration\-project"]/ul')
        
        projectlead=browser.find_element(By.PARTIAL_LINK_TEXT,"s2id_autogen")
        time.sleep(1)        
        projectlead.click()
        time.sleep(1) 
        #projectlead.send_keys(sub_project_name)        
        projectlead.send_keys("PBEL City - Phase II")
        time.sleep(1) 
        projectlead.send_keys(Keys.RETURN)
        #time.sleep(5) 
        #projectlead.select_by_visible_text("Radiance Maraikayar Manor")        
        #time.sleep(5)                
        #email=browser.find_element(By.NAME,'email')
        #email.send_keys(email1)

        #project=browser.find_element(By.XPATH,'//*[@id="basic-form-layouts"]/div/div/div/form/div/div[8]/div[3]/span/span[1]/span/span[2]').click()
        #project = browser.find_element(By.XPATH,'/html/body/span/span/span[1]/input')
        #project.send_keys(sub_project_name)
        #project.send_keys(Keys.RETURN)

        # browser.save_screenshot(save_path1)    
        # upload_an_attachment(lead_id, save_path1)
        
        submitbutton = browser.find_element(By.XPATH,'/html/body/div[1]/div[3]/div[2]/div/div[1]/div[1]/div/button')
        submitbutton.click()
        #browser.execute_script("arguments[0].click();", button)

        time.sleep(10)

        # browser.save_screenshot(save_path)    
        
        # upload_an_attachment(lead_id, save_path)
        
        return 1
    
    
    except Exception as e: 
        print(str(e))
        browser.quit()
        return -1
subproject="DLF Parc Estate"
path="."
incor(subproject, browser, site_data, lead_data, path)
