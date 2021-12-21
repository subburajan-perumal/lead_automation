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

    site_name = "casagrand"
    path = site_name
    name1 = str(first_name) + ' ' + str(last_name)

    save_paths = getsavePath(path, name1, phone, sub_project_name) 
    save_path1 = save_paths[1]
    save_path = save_paths[0]
    save_path2 = save_paths[2]

    s=Service(constants.engine)
    browser = webdriver.Firefox(service=s)
    
    if sub_project_name == "Casagrand Zenith":
        sub_project_name = 'CG Zenith'
    if sub_project_name == "Casagrand Esquire":
        sub_project_name = 'CG Esquire'
    if sub_project_name == "Casagrand Tudor":
        sub_project_name = 'CG Tudor'
    if sub_project_name == "Casagrand Savoye":
        sub_project_name = 'CG Savoye'
    if sub_project_name == "Casagrand Supremus":
        sub_project_name = 'CG Supremus'
    if sub_project_name == "Casagrand ECR 14":
        sub_project_name = 'CG ECR 14'
    if sub_project_name == "Casagrand Primera":
        sub_project_name = 'CG Primera'
    if sub_project_name == "Casagrand Crescendo Elite":
        sub_project_name = 'CG Crescendo Elite'
    if sub_project_name == "Casagrand Crecendo Compact":
        sub_project_name = 'CG Crecendo Compact'
    if sub_project_name == "Casagrand Millenia":
        sub_project_name = 'CG Millenia'
    if sub_project_name == "Casagrand Royale":
        sub_project_name = 'CG Royale'
    if sub_project_name == "Casagrand Utopia":
        sub_project_name = 'CG Utopia'
    if sub_project_name == "Casagrand Athens":
        sub_project_name = 'CG Athens'
    if sub_project_name == "Casagrand FirstCity":
        sub_project_name = 'CG FirstCity'
    

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

