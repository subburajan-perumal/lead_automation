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

    site_name = "hiranandani"
    path = "./" + site_name
    name1 = str(first_name) + ' ' + str(last_name)

    save_paths = getsavePath(path, name1, phone, sub_project_name) 
    save_path1 = save_paths[1]
    save_path = save_paths[0]
    save_path2 = save_paths[2]

    if sub_project_name == "Hiranandani Parks":
        sub_project_name = 'Hiranandani Parks'

    '''if '+91' not in phone:
        print("Not Indian Number")
        return "Failed"

    phone = phone[3:]
    '''
    #The above execuation we used to do when we wanted to accept only indian number but now we are expainding it for many country.
    
    country_code = [+91,+1,+44,+93,+880,+501,+55,+33,+49,+98,+39,+81,+962,+965,+60,+64,+65,+34,+94,+971]
    k = 0
    for i in country_code:
        #print('+'+str(i), ' ', phone[:len('+'+str(i))])
        if '+'+str(i)== phone[:len('+'+str(i))]:
            country_code = phone[:len('+'+str(i))]
            phone = phone[len('+'+str(i)):]
            k=1
     if k==0:
        return('the phonne number does not have the proper country code')


    s=Service(constants.engine)
    browser=webdriver.Firefox(service=s)

    partner = all_sites.sites[site_name]["partner_name"]
    #intrested = 'Plots'

    try:
        browser.get(all_sites.sites[site_name]["url"])

        tem = browser.find_element(By.CLASS_NAME, 'reffer-btn').click()

        name  = browser.find_element(By.NAME, "Pname")
        name.send_keys(name1)
        
        #Adding countr code
        country=  browser.find_element(By.NAME, 'cc')
        country   = Select(country)
        country.select_by_value(country_code[1:])

        contact=browser.find_element(By.NAME,'pmob')
        contact.send_keys(phone)
        #intrest_project = browser.find_element(By.ID, 'leads_project')

        intrest_project = browser.find_element(By.NAME, 'interested')
        new = Select(intrest_project)
        new.select_by_index(2)

        email=browser.find_element(By.NAME,'pemail')
        email.send_keys(email1)

        add=browser.find_element(By.XPATH,'/html/body/div[3]/div/div/div/form/div[1]/div/div/div[6]/div/div[2]/span/span').click()

        intrest_project = browser.find_element(By.NAME, 'cname')
        new = Select(intrest_project)
        new.select_by_index(2)

        
        browser.save_screenshot(save_path1)    
        upload_an_attachment(lead_id, save_path1)

        add=browser.find_element(By.XPATH,'/html/body/div[3]/div/div/div/form/button').click()
        
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
