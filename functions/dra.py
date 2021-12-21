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

    site_name = "dra"
    path = site_name
    name1 = str(first_name) + ' ' + str(last_name)

    save_paths = getsavePath(path, name1, phone, sub_project_name) 
    save_path1 = save_paths[1]
    save_path = save_paths[0]
    save_path2 = save_paths[2]

    s=Service(constants.engine)
    browser = webdriver.Firefox(service=s)

    if sub_project_name == "DRA Centralia":
        sub_project_name = 'Centralia'
    if sub_project_name == "DRA Truliv Navalur":
        sub_project_name = 'Truliv Navalur'           
    if sub_project_name == "DRA 90 Degrees":
        sub_project_name = '90 Degrees'   
    if sub_project_name == "DRA Truliv Porur":
        sub_project_name = 'Truliv Porur'   
    if sub_project_name == "DRA Truliv Navalur Commercial":
        sub_project_name = 'Truliv Navalur Commercial'   
    if sub_project_name == "Porur":
        sub_project_name = 'Truliv Porur'   
        

    '''
    all_sites.sites[site_name]["url"]
    all_sites.sites[site_name]["email"]
    all_sites.sites[site_name]["pass"]
    '''    

    try:
        browser.get(all_sites.sites[site_name]["url"])
        email = browser.find_element(By.ID, "user_email")
        email.send_keys(all_sites.sites[site_name]["email"])
        password = browser.find_element(By.ID,"user_password")
        password.send_keys(all_sites.sites[site_name]["pass"])
        browser.find_element(By.XPATH,"//button[@type='submit']").click()

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

        browser.save_screenshot(save_path1)    
        upload_an_attachment(lead_id, save_path1)

        save = browser.find_element(By.XPATH, '//*[@id="new_lead"]/div[6]/input')
        save.click()
        
        time.sleep(5)
        browser.save_screenshot(save_path) 
        browser.quit()        
        upload_an_attachment(lead_id, save_path)

        req = "Success"
        lead = Lead(name=name1, props= sub_project_name, phone = phone, email = email1, status = req, created_at =  dt_string, attachments = save_path)
        db.session.add(lead)
        db.session.commit()
        print('Successfully added' + str(lead.id) + ' ' + str(sub_project_name) + ' ' + str(lead.status))

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
