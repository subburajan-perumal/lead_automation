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


    site_name = "adityaram"
    path = "./" + site_name
    
    name1 = str(first_name) + ' ' + str(last_name)
    
    save_paths = getsavePath(path, name1, phone, sub_project_name)
    save_path1 = save_paths[1]
    save_path = save_paths[0]
    save_path2 = save_paths[2]

    if sub_project_name == "Adityaram Nagar Phase 5":
        sub_project_name = "Adityaram Nagar 5"
    if sub_project_name == "Adityaram":
        sub_project_name = "Adityaram Signature City"        
    if sub_project_name == "Adityaram Signature City":
        sub_project_name = "Adityaram Signature City"


    s=Service(constants.engine)
    browser=webdriver.Firefox(service=s)
    browser.get(all_sites.sites[site_name]["url"])

    try:
        #client name
        name=browser.find_elements(By.XPATH,'/html/body/div[1]/div/form/div[2]/div/div/input')
        name[0].send_keys(name1)
        #client email
        email=browser.find_elements(By.XPATH,'/html/body/div[1]/div/form/div[3]/div/div/input')
        email[0].send_keys(email1)
        #client contact
        contact=browser.find_elements(By.XPATH,'/html/body/div[1]/div/form/div[4]/div/div/div/input')
        contact[0].send_keys(phone)
        #CPname
        cpname1=Select(browser.find_element(By.XPATH,'/html/body/div[1]/div/form/div[5]/div[1]/div/select'))
        cpname1.select_by_visible_text(all_sites.sites[site_name]["cpname"])
        #CPphone
        cpphn1=browser.find_elements(By.XPATH,'/html/body/div[1]/div/form/div[5]/div[2]/div/input')
        cpphn1[0].send_keys(all_sites.sites[site_name]["cpphn"])
        #Project
        proj1=Select(browser.find_element(By.XPATH,'/html/body/div[1]/div/form/div[6]/div/div/select'))
        proj1.select_by_visible_text(sub_project_name)
        time.sleep(3)

        browser.save_screenshot(save_path1)    
        upload_an_attachment(lead_id, save_path1)

        add=browser.find_element(By.XPATH,'/html/body/div[1]/div/form/div[8]/div/div/input').click()
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
