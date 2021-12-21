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

    site_name = "krishnagrp"
    path = "./" + site_name
    
    name1 = str(first_name) + ' ' + str(last_name)

    save_paths = getsavePath(path, name1, phone, sub_project_name) 
    save_path1 = save_paths[1]
    save_path = save_paths[0]
    save_path2 = save_paths[2]

    s=Service(constants.engine)
    browser=webdriver.Firefox(service=s)
    
    ##browser=webdriver.Firefox(service=s)    
    #browser.get(all_sites.sites[site_name]["url"])
    
    
    if sub_project_name == "Krishna Mithila":
        sub_project_name = 'Mithila'
    if sub_project_name == "Krishna Meadows":
        sub_project_name = 'Meadows'
    if sub_project_name == "Krishna HeadQuartes":
        sub_project_name = 'HeadQuartes'
    if sub_project_name == "Krishna Tivoli Gardens":
        sub_project_name = 'Tivoli Gardens'
    if sub_project_name == "Krishna Celesta":
        sub_project_name = 'Celesta'
    
    browser.get(all_sites.sites[site_name]["url"])
    
    try:
        # Name 
        name = browser.find_element_by_xpath('//*[@id="tab-one"]/div/div[2]/div/div/div/form/div[2]/div/div/input ')
        name.send_keys(name1)
        # Email id
        mail = browser.find_element_by_xpath('//*[@id="tab-one"]/div/div[2]/div/div/div/form/div[3]/div/div/input')
        mail.send_keys(email1)
        # Project Dropdown
        project = browser.find_element_by_xpath('//*[@id="tab-one"]/div/div[2]/div/div/div/form/div[5]/div/div/select')
        project.click()
        # Phone Number
        phone = browser.find_element_by_xpath('//*[@id="tab-one"]/div/div[2]/div/div/div/form/div[4]/div/div/div/input')
        phone.send_keys(phone)
        # Channel Parter
        channelname = browser.find_element_by_xpath('//*[@id="tab-one"]/div/div[2]/div/div/div/form/div[7]/div/div/select')
        channelname.click()
        
        #channelname1 = browser.find_element_by_xpath('//*[@id="tab-one"]/div/div[2]/div/div/div/form/div[7]/div/div/select/option[2]')
        #channelname1.click()
        #Submit Button
        
        
        browser.save_screenshot(save_path1)    
        upload_an_attachment(lead_id, save_path1)
        
        submit = browser.find_element_by_xpath('/html/body/section/div/div/div[2]/div/div/div/div[2]/div/div/div/form/div[9]/div/div/ input')
        submit.click()
        time.sleep(3)
        
        print('Success')
        browser.save_screenshot(save_path)
        browser.quit()
        upload_an_attachment(lead_id, save_path)
        
        req = 'Success'
        lead = Lead(name=name1, props=sub_project_name, phone=phone,
                    email=email1, status=req, created_at=dt_string, attachments=save_path)
        db.session.add(lead)
        db.session.commit()

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

