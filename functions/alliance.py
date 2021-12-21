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

    site_name = "alliance"
    path = "./" + site_name
    
    name1 = str(first_name) + ' ' + str(last_name)
    
    save_paths = getsavePath(path, name1, phone, sub_project_name) 
    save_path1 = save_paths[1]
    save_path = save_paths[0]
    save_path2 = save_paths[2]

    
    if sub_project_name == "Alliance Humming Gardens": ## FROM CRM
        sub_project_name = 'Humming Gardens'            ## FROM PARTNER PORTAL
    if sub_project_name == "Alliance Galleria":
        sub_project_name = 'Alliance Galleria Residences'
    if sub_project_name == "Urbanrise Eternity":
        sub_project_name = 'Villabelvedere/Eternity'
    if sub_project_name == "alliancegalleria":
        sub_project_name = 'Alliance Galleria Residences'
    if sub_project_name == "OMR":
        sub_project_name = 'OMR Cluster - JS/CNCB,CNGS'
    if sub_project_name == "Sholinganallur":
        sub_project_name = 'OMR Cluster - JS/CNCB,CNGS'


    if '+91' in phone:
        phone = phone[3:]

    s=Service(constants.engine)

    '''
    all_sites.sites[site_name]["url"]
    all_sites.sites[site_name]["email"]
    all_sites.sites[site_name]["pass"]
    '''    

    try:
        browser=webdriver.Firefox(service=s)
        browser.get(all_sites.sites[site_name]["url"])
        search=browser.find_element(By.ID,'email')
        search.send_keys(all_sites.sites[site_name]["email"])
        passo=browser.find_element(By.ID,'password')
        passo.send_keys(all_sites.sites[site_name]["pass"])
        submit=browser.find_element(By.ID,'digit_login_signin_submit')
        submit.send_keys(Keys.RETURN)
        time.sleep(10)
        lead=browser.find_elements(By.CLASS_NAME,'kt-menu__item')
        lead[1].click()
        time.sleep(5)
        name=browser.find_element(By.NAME,'name')
        name.send_keys(name1)
        contact=browser.find_element(By.NAME,'contact')
        contact.send_keys(phone)
        email=browser.find_element(By.NAME,'email')
        email.send_keys(email1)
        project=Select(browser.find_element(By.ID,'select_project'))
        project.select_by_visible_text(sub_project_name)

        browser.save_screenshot(save_path1)    
        upload_an_attachment(lead_id, save_path1)

        add=browser.find_element(By.ID,'lead_submit_btn').click()
        aa = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.XPATH,"//*[@id='kt_table_1']/tbody/tr[1]/td[7]"))
        )
        req=aa.text
        aa.click()
        
        time.sleep(5) ## FOR CHANGING WAIT TIME
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
