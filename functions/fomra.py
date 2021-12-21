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

    site_name = "fomra"
    path = "./" + site_name
    name1 = str(first_name) + ' ' + str(last_name)
    
    save_paths = getsavePath(path, name1, phone, sub_project_name) 
    save_path1 = save_paths[1]
    save_path = save_paths[0]
    save_path2 = save_paths[2]

    
    if sub_project_name == "Fomra Hues":
        sub_project_name = 'Hues'
    if sub_project_name == "Fomra Celebration":
        sub_project_name = 'Celebration'
    if sub_project_name == "Fomra Vayou":
        sub_project_name = 'Vayou'

    s=Service(constants.engine)

    '''
    all_sites.sites[site_name]["url"]
    all_sites.sites[site_name]["email"]
    all_sites.sites[site_name]["pass"]
    '''

    try:
        browser=webdriver.Firefox(service=s)
        browser.get(all_sites.sites[site_name]["url"])
        client_name=browser.find_element(By.XPATH,'/html/body/div/div/div/div/div/div/div/form/div[2]/div/div/input[1]')
        client_name.send_keys(name1)
        client_email=browser.find_element(By.XPATH,'/html/body/div/div/div/div/div/div/div/form/div[3]/div/div/input')
        client_email.send_keys(email1)
        client_phone=browser.find_element(By.XPATH,'//html/body/div/div/div/div/div/div/div/form/div[4]/div/div/div/input')
        client_phone.send_keys(phone)
        channel_pn=Select(browser.find_element(By.XPATH,'/html/body/div/div/div/div/div/div/div/form/div[5]/div/div/select'))
        channel_pn.select_by_visible_text(sub_project_name)
        project=Select(browser.find_element(By.XPATH,'/html/body/div/div/div/div/div/div/div/form/div[7]/div/div/select'))
        project.select_by_visible_text(all_sites.sites[site_name]["partner_name"])
        channel_phone=Select(browser.find_element(By.XPATH,'/html/body/div/div/div/div/div/div/div/form/div[8]/div/div/input'))
        channel_phone.send_keys(all_sites.sites[site_name]["channel_phone_number"])

        
        browser.save_screenshot(save_path1)    
        upload_an_attachment(lead_id, save_path1)

        submit=browser.find_element(By.XPATH,'/html/body/div/div/div/div/div/div/div/form/div[9]/div/div/input').click()
        time.sleep(10)

        print('success')
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
