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

    site_name = "doshi"
    path = "./" + site_name
    name1 = str(first_name) + ' ' + str(last_name)

    save_paths = getsavePath(path, name1, phone, sub_project_name) 
    save_path1 = save_paths[1]
    save_path = save_paths[0]
    save_path2 = save_paths[2]    

    s=Service(constants.engine)
    browser=webdriver.Firefox(service=s)

    if sub_project_name == "Doshi Serene County":
        sub_project_name = 'SERENE COUNTY'
        #val = '9'
    if sub_project_name == "Doshi Risington":
        sub_project_name = 'RISINGTON'
        #val = '13'        
    if sub_project_name == "Doshi First Nest":
        sub_project_name = 'FIRSTNEST'
        #val = '11'


    try:
        browser.get(all_sites.sites[site_name]["url"])
        search=browser.find_element(By.ID,'username')
        search.send_keys(all_sites.sites[site_name]["email"])
        passo=browser.find_element(By.ID,'password')
        passo.send_keys(all_sites.sites[site_name]["pass"])
        submit=browser.find_element(By.NAME,'user_login').click()

        #submit.send_keys(Keys.RETURN)
        time.sleep(2)
        lead=browser.find_elements(By.CLASS_NAME,'icon-plus')[0].click()
        time.sleep(2)

        name  = browser.find_element(By.NAME, "leads_name")
        name.send_keys(name1)
        contact=browser.find_element(By.NAME,'leads_mobile_number')
        contact.send_keys(phone)
        #intrest_project = browser.find_element(By.ID, 'leads_project')

        '''
        alt_contact = browser.find_element(By.NAME, 'leads_phone_number')
        alt_contact.send_keys(alternet_contact)
        '''

        email=browser.find_element(By.NAME,'leads_email')
        email.send_keys(email1)

        '''
        whatsapp_contact = browser.find_element(By.NAME, 'leads_whatsapp')
        whatsapp_contact.send_keys(whatsapp)

        
        adress = browser.find_element(By.NAME, 'leads_address_two')
        adress.send_keys(address_contact)

        unit = browser.find_element(By.NAME, 'leads_unit')
        unit.send_keys(unit_type)


        remark = browser.find_element(By.NAME, 'leads_remarks')
        remark.send_keys(remark_enter)
        '''

        #tem = browser.find_element(By.XPATH, '/html/body/div[7]/div/div/div/form/div[2]/div[3]/div[3]/select')
        #sct = Select(tem)
        #sct.select_by_value(val)

        tem = browser.find_element(By.XPATH, '/html/body/div[7]/div/div/div/form/div[2]/div[3]/div[3]/select')
        sct = Select(tem)
        sct.select_by_visible_text(sub_project_name)

        #project=Select(browser.find_element(By.ID,'select_project'))
        #project.select_by_visible_text(project_name)

        
        browser.save_screenshot(save_path1)    
        upload_an_attachment(lead_id, save_path1)

        add=browser.find_element(By.NAME,'leads_add').click()
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
