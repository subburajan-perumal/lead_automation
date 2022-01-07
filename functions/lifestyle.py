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

    site_name = "lifestyle"
    path = "./" + site_name
    
    name1 = str(first_name) + ' ' + str(last_name)

    save_paths = getsavePath(path, name1, phone, sub_project_name) 
    save_path1 = save_paths[1]
    save_path = save_paths[0]
    save_path2 = save_paths[2]

    if sub_project_name == "Lifestyle LeParadis":
        sub_project_name = 'Lifestyle LeParadis'
    if sub_project_name == "Lifestyle Podium":
        sub_project_name = "Lifestyle Podium"
    if sub_project_name == "Podium":
        sub_project_name = "Lifestyle Podium"        
    if sub_project_name == "Porur":
        sub_project_name = 'Lifestyle LeParadis'
        
    '''
    if '+91' not in phone:
        print("Not Indian Number")
        return "Failed"

    phone = phone[3:]
    '''
    country_code = [+91,+1,+44,+93,+880,+501,+55,+33,+49,+98,+39,+81,+962,+965,+60,+64,+65,+34,+94,+971]

    for i in country_code:
        #print('+'+str(i), ' ', phone[:len('+'+str(i))])
        if '+'+str(i)== phone[:len('+'+str(i))]:
            country_code = phone[:len('+'+str(i))]
            phone = phone[len('+'+str(i)):]
            
    
    alternet_contact = phone
    whatsapp = phone
    remark = "NIL"
    project_intrested = sub_project_name
    #flat_type = '1 BHK'
    enquiry_sourse = 'Channel Partner'
    enquiry_owner  = 'LeadAutomation'
    #location = 'A'
    #budget = 'Below 5'
    #enquiry_Medium = 'Server Call'
    #channel_partner = 'LeadAutomation'

    s=Service(constants.engine)
    browser=webdriver.Firefox(service=s)


    try:
        browser.get(all_sites.sites[site_name]["url"])
        search=browser.find_element(By.ID,'username')
        search.send_keys(all_sites.sites[site_name]["email"])
        passo=browser.find_element(By.ID,'password')
        passo.send_keys(all_sites.sites[site_name]["pass"])
        submit=browser.find_element(By.CLASS_NAME,'signin-button').click()

        #submit.send_keys(Keys.RETURN)
        time.sleep(2)
        lead=browser.find_elements(By.ID,'menubar_item_Appointments')[1].click()
        time.sleep(2)

        adding=browser.find_element(By.CLASS_NAME,'icon-plus')
        adding.click()
        time.sleep(2)
        
        #Adding the country code
        country1=  browser.find_element(By.XPATH, '/html/body/div[2]/div[3]/div/div[2]/div[2]/form/table[1]/tbody/tr[1]/td[4]/div/span/div/a/div/b')
        country1.click()
        country2 = browser.find_element(By.XPATH, '/html/body/div[2]/div[3]/div/div[2]/div[2]/form/table[1]/tbody/tr[1]/td[4]/div/span/div/div/div/input')
        country2.send_keys(country_code)
        country2.send_keys(Keys.RETURN)
        
        #Adding phone number
        name  = browser.find_element(By.NAME, "contactname")
        name.send_keys(name1)
        contact=browser.find_element(By.NAME,'mobile')
        contact.send_keys(phone)

        intrest_project = browser.find_element(By.XPATH, '/html/body/div[2]/div[3]/div/div[2]/div[2]/form/table[1]/tbody/tr[2]/td[2]/div/span/div/a/div/b')
        intrest_project.click()
        new = browser.find_element(By.XPATH, '/html/body/div[2]/div[3]/div/div[2]/div[2]/form/table[1]/tbody/tr[2]/td[2]/div/span/div/div/div/input')
        new.send_keys(project_intrested)
        new.send_keys(Keys.RETURN)

        intrest_project = browser.find_element(By.XPATH, '/html/body/div[2]/div[3]/div/div[2]/div[2]/form/table[1]/tbody/tr[2]/td[4]/div/span/div/a/div/b')
        intrest_project.click()
        new = browser.find_element(By.XPATH, '/html/body/div[2]/div[3]/div/div[2]/div[2]/form/table[1]/tbody/tr[2]/td[4]/div/span/div/div/div/input')
        new.send_keys(enquiry_owner)
        new.send_keys(Keys.RETURN)

        '''
        alt_contact = browser.find_element(By.NAME, 'altmobile')
        alt_contact.send_keys(alternet_contact)
        '''
        
        email=browser.find_element(By.NAME,'email')
        email.send_keys(email1)

        '''
        whatsapp_contact = browser.find_element(By.NAME, 'whatsapp')
        whatsapp_contact.send_keys(whatsapp)
        '''

        intrest_project = browser.find_element(By.XPATH, '/html/body/div[2]/div[3]/div/div[2]/div[2]/form/table[1]/tbody/tr[4]/td[4]/div/span/div/a/div/b')
        intrest_project.click()

        '''
        new = browser.find_element(By.XPATH, '/html/body/div[2]/div[3]/div/div[2]/div[2]/form/table[1]/tbody/tr[4]/td[4]/div/span/div/div/div/input')
        new.send_keys(location)
        new.send_keys(Keys.RETURN)
        '''

        intrest_project = browser.find_element(By.XPATH, '/html/body/div[2]/div[3]/div/div[2]/div[2]/form/table[1]/tbody/tr[5]/td[2]/div/span/div/a/div/b')
        intrest_project.click()

        '''
        new = browser.find_element(By.XPATH, '/html/body/div[2]/div[3]/div/div[2]/div[2]/form/table[1]/tbody/tr[5]/td[2]/div/span/div/div/div/input')
        new.send_keys(flat_type)
        new.send_keys(Keys.RETURN)
        '''

        '''
        #Budget
        intrest_project = browser.find_element(By.XPATH, '/html/body/div[2]/div[3]/div/div[2]/div[2]/form/table[1]/tbody/tr[5]/td[4]/div/span/div/a/div/b')
        intrest_project.click()
        new = browser.find_element(By.XPATH, '/html/body/div[2]/div[3]/div/div[2]/div[2]/form/table[1]/tbody/tr[5]/td[4]/div/span/div/div/div/input')
        new.send_keys(budget)
        new.send_keys(Keys.RETURN)
        '''

        '''
        #Enqiry Souce
        intrest_project = browser.find_element(By.XPATH, '/html/body/div[2]/div[3]/div/div[2]/div[2]/form/table[1]/tbody/tr[6]/td[2]/div/span/div/a/div/b')
        intrest_project.click()
        new = browser.find_element(By.XPATH, '/html/body/div[2]/div[3]/div/div[2]/div[2]/form/table[1]/tbody/tr[6]/td[2]/div/span/div/div/div/input')
        new.send_keys(enquiry_sourse)
        new.send_keys(Keys.RETURN)

        #Enqiry Medium
        intrest_project = browser.find_element(By.XPATH, '/html/body/div[2]/div[3]/div/div[2]/div[2]/form/table[1]/tbody/tr[6]/td[4]/div/span/div/a/div/b')
        intrest_project.click()
        new = browser.find_element(By.XPATH, '/html/body/div[2]/div[3]/div/div[2]/div[2]/form/table[1]/tbody/tr[6]/td[4]/div/span/div/div/div/input')
        new.send_keys(enquiry_Medium)
        new.send_keys(Keys.RETURN)

        #Enqiry Status
        intrest_project = browser.find_element(By.XPATH, '/html/body/div[2]/div[3]/div/div[2]/div[2]/form/table[1]/tbody/tr[7]/td[2]/div/span/div/a/div/b')
        intrest_project.click()
        new = browser.find_element(By.XPATH, '/html/body/div[2]/div[3]/div/div[2]/div[2]/form/table[1]/tbody/tr[7]/td[2]/div/span/div/div/div/input')
        new.send_keys(enquiry_Medium)
        new.send_keys(Keys.RETURN)
        '''

        #Channel Partner
        intrest_project = browser.find_element(By.XPATH, '/html/body/div[2]/div[3]/div/div[2]/div[2]/form/table[1]/tbody/tr[7]/td[4]/div/span/div/a/div/b')
        intrest_project.click()
        new = browser.find_element(By.XPATH, '/html/body/div[2]/div[3]/div/div[2]/div[2]/form/table[1]/tbody/tr[7]/td[4]/div/span/div/div/div/input')
        new.send_keys(all_sites.sites[site_name]["channel_partner"])
        new.send_keys(Keys.RETURN)

        #project=Select(browser.find_element(By.XPATH,'//*[@id="Appointments_editView_fieldName_description"]'))
        #project.select_by_visible_text(remark)
        
        
        browser.save_screenshot(save_path1)    
        upload_an_attachment(lead_id, save_path1)
        
        add=browser.find_element(By.XPATH,'/html/body/div[2]/div[3]/div/div[2]/div[2]/form/div[2]/div[1]/button/strong').click()
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
