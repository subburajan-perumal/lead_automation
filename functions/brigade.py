def fin_function(lead_id, sub_project_name, first_name, last_name, phone, email1):
    from data import all_sites
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.support.ui import Select
    from selenium.webdriver.firefox.options import Options
    import time
    from full import db, Lead
    from data import constants
    from functions.util import getTime
    from functions.util import upload_an_attachment, send_mail, getsavePath

    dt_string = getTime()
    
    site_name = "brigade"
    path = "./" + site_name
    
    save_paths = getsavePath(path, last_name, phone, sub_project_name) 
    save_path1 = save_paths[1]
    save_path = save_paths[0]
    save_path2 = save_paths[2]

    first_name = last_name
    name1 = first_name
    
    if sub_project_name == "Brigade Xanadu":
        sub_project_name = "Brigade Xanadu"
    if sub_project_name == "Brigade Bonito":
        sub_project_name = "Brigade Xanadu"
    if sub_project_name == "Brigade Residences at WTC":
        sub_project_name = "WTC Residences Chennai"    
    if sub_project_name == "Brigade Residences":
        sub_project_name = "WTC Residences Chennai"           
    if sub_project_name == "brigade-":
        sub_project_name = "Brigade Xanadu"
    
    s=Service(constants.engine)
    browser=webdriver.Firefox(service=s)
    browser.get(all_sites.sites[site_name]["url"])
    
    try:
        #company name
        company_name = browser.find_element(By.XPATH,'//*[@id="input_5"]')
        company_name.send_keys(all_sites.sites[site_name]["company"])
        #agent name
        agentf = browser.find_elements(By.XPATH,'//*[@id="first_6"]')
        agentf[0].send_keys(all_sites.sites[site_name]["agentf1"])
        agentl = browser.find_elements(By.XPATH,'//*[@id="last_6"]')
        agentl[0].send_keys(all_sites.sites[site_name]["agentl1"])
        
        #agent mobile number
        aph11 = browser.find_elements(By.XPATH,'//*[@id="input_7_country"]')
        aph11[0].send_keys(all_sites.sites[site_name]["aph1"])
        aph21 = browser.find_elements(By.XPATH,'//*[@id="input_7_area"]')
        aph21[0].send_keys(all_sites.sites[site_name]["aph2"])
        aph31 = browser.find_elements(By.XPATH,'//*[@id="input_7_phone"]')
        aph31[0].send_keys(all_sites.sites[site_name]["aph3"])
        
        #agent email
        amail1 = browser.find_elements(By.XPATH,'//*[@id="input_8"]')
        amail1[0].send_keys(all_sites.sites[site_name]["email"])
        
        #client name
        fname=browser.find_element(By.XPATH,'//*[@id="first_11"]')
        fname.send_keys(first_name)
        lname = browser.find_element(By.ID,'last_11')
        lname.send_keys(last_name)
        
        #mobile number 1
        aph1c = browser.find_element(By.XPATH,'//*[@id="input_12_country"]')
        aph1c.send_keys(all_sites.sites[site_name]["aph1"])
        aph2c = browser.find_element(By.XPATH,'//*[@id="input_12_area"]')
        aph2c.send_keys(all_sites.sites[site_name]["aph2"])
        aph3c = browser.find_element(By.XPATH,'//*[@id="input_12_phone"]')
        aph3c.send_keys(phone)
        
        #mobile number 2
        aph1c2 = browser.find_element(By.XPATH,'//*[@id="input_14_country"]')
        aph1c2.send_keys(all_sites.sites[site_name]["aph1"])
        aph2c2 = browser.find_element(By.XPATH,'//*[@id="input_14_area"]')
        aph2c2.send_keys(all_sites.sites[site_name]["aph2"])
        aph3c2 = browser.find_element(By.XPATH,'//*[@id="input_14_phone"]')
        aph3c2.send_keys(phone)
        
        #emails
        email11=browser.find_element(By.XPATH,'//*[@id="input_13"]')
        email11.send_keys(email1)
        email21=browser.find_element(By.XPATH,'//*[@id="input_15"]')
        email21.send_keys(email1)
        
        #project name
        project=Select(browser.find_element(By.XPATH,'//*[@id="input_16"]'))
        project.select_by_visible_text(sub_project_name)

        browser.save_screenshot(save_path1)    
        upload_an_attachment(lead_id, save_path1)

        add=browser.find_element(By.XPATH,'//*[@id="input_2"]').click()
        
        time.sleep(10)
        browser.save_screenshot(save_path)
        browser.quit()
        upload_an_attachment(lead_id, save_path)

        req = "Success"
        lead = Lead(name=name1, props= sub_project_name, phone = phone, email = email1, status = req, created_at =  dt_string, attachments = save_path)
        db.session.add(lead)
        db.session.commit()
        print('Successfully added ' + str(lead.id) + ' ' + str(sub_project_name) + ' ' + str(lead.status))

    except:
        browser.save_screenshot(save_path2)
        browser.quit()
        req = 'Failed'
        lead = Lead(name=name1, props=sub_project_name, phone=phone,
                    email=email1, status=req, created_at=dt_string, attachments=save_path2)
        db.session.add(lead)
        db.session.commit()
        print('Unknown Error' + str(lead.id) + ' ' +
              str(sub_project_name) + ' ' + str(lead.status))
        send_mail(lead_id, save_path2, sub_project_name, name1)

        upload_an_attachment(lead_id, save_path2)

    return 'Success'
