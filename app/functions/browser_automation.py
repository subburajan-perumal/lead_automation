import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from app.util.utility import getName



def akshaya(subproject, browser, site_data, lead_data,automate_path):
    try:
        save_path = automate_path
        fullname=str(lead_data['name'])
        first_name,last_name=getName(fullname)
        browser.get(site_data["url"])
        fl_email = browser.find_element(By.ID, "user_email")
        fl_email.send_keys(site_data["email"])
        fl_password = browser.find_element(By.ID, "user_password")
        fl_password.send_keys(site_data["pass"])
        browser.find_element(By.XPATH, "//button[@type='submit']").click()
        f_Leads = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, "Leads")))
        # f_Leads = browser.find_element(By.LINK_TEXT, "Leads")
        f_Leads.click()
        f_addlead = browser.find_element(
            By.XPATH, "//a[@href='/broker/2150/leads/new']")
        f_addlead.click()
        f_firstname = browser.find_element(By.ID, "lead_first_name")
        f_firstname.send_keys(first_name)
        f_lastname = browser.find_element(By.ID, "lead_last_name")
        f_lastname.send_keys(last_name)
        f_mail = browser.find_element(
            By.XPATH, '/html/body/div[1]/div/div[2]/form/div[2]/div[2]/div[2]/div[1]/div/div/a')
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

        browser.save_screenshot(save_path[0])
        browser.implicitly_wait(5)
        browser.save_screenshot(save_path[1])
        browser.close()
        return 1

    except Exception as e:
        time.sleep(5)
        browser.save_screenshot(save_path[2])
        browser.close()
        return -1


def brigade(subproject, browser, site_data, lead_data,automate_path):         
    try:    
        
        save_path = automate_path
        fullname=str(lead_data['name'])
        first_name,last_name=getName(fullname)
        
    #browser# yield "on working"
        save_path=automate_path
        browser.get(site_data["url"])
        company_name = browser.find_element(By.XPATH,'//*[@id="input_5"]')
        company_name.send_keys(site_data["company"])
        #agent name
        f_agentf = browser.find_elements(By.XPATH,'//*[@id="first_6"]')
        f_agentf[0].send_keys(site_data["agentf1"])
        f_agentl = browser.find_elements(By.XPATH,'//*[@id="last_6"]')
        f_agentl[0].send_keys(site_data["agentl1"])
        
        #agent mobile number
        f_aph11 = browser.find_elements(By.XPATH,'//*[@id="input_7_country"]')
        f_aph11[0].send_keys(site_data["aph1"])
        f_aph21 = browser.find_elements(By.XPATH,'//*[@id="input_7_area"]')
        f_aph21[0].send_keys(site_data["aph2"])
        f_aph31 = browser.find_elements(By.XPATH,'//*[@id="input_7_phone"]')
        f_aph31[0].send_keys(site_data["aph3"])
        
        #agent email
        f_mail = browser.find_elements(By.XPATH,'//*[@id="input_8"]')
        f_mail[0].send_keys(site_data["email"])
        
        #client name
        f_firstname=browser.find_element(By.XPATH,'//*[@id="first_11"]')
        f_firstname.send_keys(lead_data['name'])
        f_lastname = browser.find_element(By.ID,'last_11')
        f_lastname.send_keys(lead_data['name'])
        
        #mobile number 1
        f_aph1c = browser.find_element(By.XPATH,'//*[@id="input_12_country"]')
        f_aph1c.send_keys(site_data["aph1"])
        f_aph2c = browser.find_element(By.XPATH,'//*[@id="input_12_area"]')
        f_aph2c.send_keys(site_data["aph2"])
        f_aph3c = browser.find_element(By.XPATH,'//*[@id="input_12_phone"]')
        f_aph3c.send_keys(lead_data["phone"])
        
        #mobile number 2
        f_aph1c2 = browser.find_element(By.XPATH,'//*[@id="input_14_country"]')
        f_aph1c2.send_keys(site_data["aph1"])
        f_aph2c2 = browser.find_element(By.XPATH,'//*[@id="input_14_area"]')
        f_aph2c2.send_keys(site_data["aph2"])
        f_aph3c2 = browser.find_element(By.XPATH,'//*[@id="input_14_phone"]')
        f_aph3c2.send_keys(lead_data["phone"])
        
        #emails
        f_email11=browser.find_element(By.XPATH,'//*[@id="input_13"]')
        f_email11.send_keys(lead_data["email"])
        f_email21=browser.find_element(By.XPATH,'//*[@id="input_15"]')
        f_email21.send_keys(lead_data["email"])
        
        #project name
        project=Select(browser.find_element(By.XPATH,'//*[@id="input_16"]'))
        project.select_by_visible_text(subproject)

        browser.save_screenshot(save_path[0])    

        # f_add=browser.find_element(By.XPATH,'//*[@id="input_2"]').click()
        browser.implicitly_wait(5)
        # time.sleep(10)
        browser.save_screenshot(save_path[1])
        browser.close()
        print("brigage website work successfully")
        return 1
    except Exception as e:
        time((5))
        browser.save_screenshot(save_path[2])
    
        return -1

def fomra(subproject, browser, site_data, lead_data, automate_path):
    try:
        save_path = automate_path
        fullname=str(lead_data['name'])
        first_name,last_name=getName(fullname)
        browser.get(site_data['url'])
        f_name=browser.find_element(By.XPATH,'/html/body/div/div/div/div/div/div/div/form/div[2]/div/div/input[1]')
        f_name.send_keys(fullname)
        f_email=browser.find_element(By.XPATH,'/html/body/div/div/div/div/div/div/div/form/div[3]/div/div/input')
        f_email.send_keys(lead_data['email'])
        f_phone=browser.find_element(By.XPATH,'//html/body/div/div/div/div/div/div/div/form/div[4]/div/div/div/input')
        f_phone.send_keys(lead_data['phone'])
        f_project=Select(browser.find_element(By.XPATH,'/html/body/div/div/div/div/div/div/div/form/div[7]/div/div/select'))
        f_project.select_by_visible_text(site_data["partner_name"])
        
        f_channel_pn=Select(browser.find_element(By.XPATH,'/html/body/div/div/div/div/div/div/div/form/div[5]/div/div/select'))
        f_channel_pn.select_by_visible_text(subproject)
        
        f_channel_phone=browser.find_element(By.XPATH,'/html/body/div/div/div/div/div/div/div/form/div[8]/div/div/input')
        f_channel_phone.send_keys(site_data["channel_phone_number"])

        
        browser.save_screenshot(save_path[0])    
    

        submit=browser.find_element(By.XPATH,'/html/body/div/div/div/div/div/div/div/form/div[9]/div/div/input').click()
        time.sleep(5)
        # browser.implicitly_wait(5)

        
        browser.save_screenshot(save_path[1])
        browser.close()
        return 1
    except Exception as e:
        time.sleep(5)
        browser.save_screenshot(save_path[2])

        return -1

def alliance(subproject, browser, site_data, lead_data, automate_path):
    try:
        save_path = automate_path
        fullname=str(lead_data['name'])
        first_name,last_name=getName(fullname)
        browser.get(site_data["url"])
        fl_search=browser.find_element(By.ID,'email')
        fl_search.send_keys(site_data["email"])
        fl_passo=browser.find_element(By.ID,'password')
        fl_passo.send_keys(site_data["pass"])
        fs_submit=browser.find_element(By.ID,'digit_login_signin_submit')
        fs_submit.send_keys(Keys.RETURN)
        time.sleep(10)
        f_lead=browser.find_elements(By.CLASS_NAME,'kt-menu__item')
        f_lead[1].click()
        time.sleep(5)
        f_name=browser.find_element(By.NAME,'name')
        f_name.send_keys(lead_data['name'])
        contact=browser.find_element(By.NAME,'contact')
        contact.send_keys(lead_data['phone'])
        email=browser.find_element(By.NAME,'email')
        email.send_keys(lead_data['email'])
        project=Select(browser.find_element(By.ID,'select_project'))
        project.select_by_visible_text(subproject)

        browser.save_screenshot(save_path[0])    

        add=browser.find_element(By.ID,'lead_submit_btn').click()
        aa = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.XPATH,"//*[@id='kt_table_1']/tbody/tr[1]/td[7]"))
        )
        # browser.save_screenshot(save_path[0])
        aa.click()
        
        time.sleep(5) ## FOR CHANGING WAIT TIME
        browser.save_screenshot(save_path[1])
        browser.close()
        return 1
    except Exception as e:
        browser.save_screenshot(save_path[2])
        return -1



def casagrand(subproject, browser, site_data, lead_data, automate_path):
    try:
        save_path = automate_path
        fullname=str(lead_data['name'])
        first_name,last_name=getName(fullname)
        browser.get(site_data["url"])
        fl_email = browser.find_element(By.ID, "user_email")
        fl_email.send_keys(site_data["email"])
        fl_password = browser.find_element(By.ID,"user_password")
        fl_password.send_keys(site_data["pass"])
        browser.find_element(By.XPATH,"//button[@type='submit']").click()

        Leads = browser.find_element(By.LINK_TEXT, "Leads")
        Leads.click()
        addlead = browser.find_element(By.XPATH, "/html/body/div/div/div[1]/div/ul/li/ul/li[2]/a")
        addlead.click()

        firstname = browser.find_element(By.ID, "lead_first_name")
        firstname.send_keys(fullname)
        lastname = browser.find_element(By.ID, "lead_last_name")
        lastname.send_keys(fullname)

        #nri = browser.find_element(By.ID, "lead_nri")
        #nri.click()
        #nri.click()

        f_mail = browser.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/form/div[2]/div[2]/div[2]/div[1]/div/div/a')
        f_mail.click()
        f_alt_mail = browser.find_element(By.XPATH, '/html/body/div[3]/div/input')
        f_alt_mail.click()
        f_alt_mail.send_keys(lead_data['email'])
        f_alt_mail.send_keys(Keys.RETURN)
        f_phone = browser.find_element(By.XPATH, '//*[@id="lead_phone"]')
        f_phone.click()
        f_phone.send_keys(lead_data['phone'])
        button2 = browser.find_element(By.XPATH, '//*[@id="s2id_lead_project_ids"]/a/span[2]')
        button2.click()
        f_project = browser.find_element(By.XPATH, '/html/body/div[4]/div/input')
        f_project.send_keys(subproject)
        f_project.send_keys(Keys.RETURN)

        browser.save_screenshot(save_path[0])    
    

        fs_save = browser.find_element(By.XPATH, '//*[@id="new_lead"]/div[6]/input')
        fs_save.click()
        
        time.sleep(5)
        browser.save_screenshot(save_path[1])
        browser.close()
        return 1
    except Exception as e:
        browser.save_screenshot(save_path[2])
        return -1