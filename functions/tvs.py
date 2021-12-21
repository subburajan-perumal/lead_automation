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
    from selenium.webdriver.common.alert import Alert
    import time
    from full import db, Lead
    from data import constants
    from functions.util import getTime
    from functions.util import upload_an_attachment, send_mail, getsavePath

    dt_string = getTime()

    site_name = "tvs"
    path = "./" + site_name

    name1 = str(first_name) + ' ' + str(last_name)

    save_paths = getsavePath(path, name1, phone, sub_project_name) 
    save_path1 = save_paths[1]
    save_path = save_paths[0]
    save_path2 = save_paths[2]


    if sub_project_name == "TVS Emerald GreenAcres Apts":
        sub_project_name = 'TVS Emerald GreenAcres Apts'
    if sub_project_name == "TVS Emerald Green Enclave":
        sub_project_name = 'TVS Emerald Green Enclave'
    if sub_project_name == "TVS Emerald LightHouse":
        sub_project_name = 'TVS Emerald LightHouse'
    if sub_project_name == "TVS Emerald Peninsula":
        sub_project_name = 'TVS Emerald Manapakkam'
    if sub_project_name == "Tvs Emerald Hamlet" or sub_project_name == "TVS Emerald Hamlet":
        sub_project_name = 'TVS Emerald Hamlet'
    if sub_project_name == "Porur":
        sub_project_name = 'TVS Emerald Green Enclave'
    if sub_project_name == "Green Enclave":
        sub_project_name = 'TVS Emerald Green Enclave'

    if '+91' in phone:
        phone = phone[3:]

    s=Service(constants.engine)
    '''
    all_sites.sites[site_name]["url"]
    all_sites.sites[site_name]["email"]
    all_sites.sites[site_name]["pass"]
    '''
    browser=webdriver.Firefox(service=s)    
    browser.get(all_sites.sites[site_name]["url"])

    try:
        client_name=browser.find_element(By.XPATH,'/html/body/div/div/div/div/div/div/div/form/div[2]/div/div/input[1]')
        client_name.send_keys(name1)
        client_email=browser.find_element(By.XPATH,'/html/body/div/div/div/div/div/div/div/form/div[3]/div/div/input')
        client_email.send_keys(email1)
        client_phone=browser.find_element(By.XPATH,'//html/body/div/div/div/div/div/div/div/form/div[4]/div/div/div/input')
        client_phone.send_keys(phone)
        project=Select(browser.find_element(By.XPATH,'/html/body/div/div/div/div/div/div/div/form/div[5]/div/div/select'))
        project.select_by_visible_text(sub_project_name)
        channel_name=browser.find_element(By.XPATH,'/html/body/div/div/div/div/div/div/div/form/div[6]/div/div/input')
        channel_name.send_keys(all_sites.sites[site_name]["cpname"])
        channel_phone=browser.find_element(By.XPATH,'/html/body/div/div/div/div/div/div/div/form/div[7]/div/div/input')
        channel_phone.send_keys(all_sites.sites[site_name]["cpphn"])
        comment=browser.find_element(By.XPATH,'/html/body/div/div/div/div/div/div/div/form/div[8]/div/div/textarea')
        comment.send_keys('Nil')
        
        browser.save_screenshot(save_path1)    
        upload_an_attachment(lead_id, save_path1)
        time.sleep(2)

        submit = browser.find_element(By.XPATH, '/html/body/div/div/div/div/div/div/div/form/div[9]/div/div/input')
        submit.click()
        time.sleep(4)

        try:
            alert = Alert(browser)
            #print(alert.text)
            browser.save_screenshot(save_path)
            alert.accept()
            time.sleep(5)
            browser.quit()
            upload_an_attachment(lead_id, save_path)
            send_mail(lead_id, save_path2, sub_project_name, name1)
            req = 'Failed'
        except:
            time.sleep(5)
            browser.save_screenshot(save_path)
            browser.quit()
            upload_an_attachment(lead_id, save_path)
            req = 'Success'
        
        lead = Lead(name=name1, props=sub_project_name, phone=phone,
                    email=email1, status=req, created_at=dt_string, attachments=save_path)
        db.session.add(lead)
        db.session.commit()
        print('Successfully added' + str(lead.id) + ' ' +
                str(sub_project_name) + ' ' + str(lead.status))

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
