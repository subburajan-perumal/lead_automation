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

    site_name = "radiance"
    path = "./" + site_name
    
    name1 = str(first_name) + ' ' + str(last_name)

    save_paths = getsavePath(path, name1, phone, sub_project_name) 
    save_path1 = save_paths[1]
    save_path = save_paths[0]
    save_path2 = save_paths[2]


    ## ADD COUNTRIES HERE
    
    country_name = 'India'

    if '+91' in phone:
        country_name = 'India'
        phone = phone[3:]
    if '+1' in phone:
        country_name = 'United States'
        phone = phone[2:]
    if '+44' in phone:
        country_name = 'United Kingdom'
        phone = phone[3:]    
    if '+971' in phone:
        country_name = 'United Arab Emirates'
        phone = phone[4:] 


    ### ADD PROPERTIES HERE

    if sub_project_name == "Radiance Elite":
        sub_project_name = 'Radiance Elite'
    if sub_project_name == "Radiance Splendour":
        sub_project_name = 'Radiance Splendour'
    if sub_project_name == "Radiance Smartville":
        sub_project_name = 'Radiance Smartville'
    if sub_project_name == "Radiance The Pride":
        sub_project_name = 'Radiance The Pride'    
    if sub_project_name == "Radiance Suprema":
        sub_project_name = 'Radiance Suprema'
    if sub_project_name == "Radiance Blossom":
        sub_project_name = 'Radiance Blossom'
    if sub_project_name == "Radiance Sapphire":
        sub_project_name = 'Radiance Sapphire'
    if sub_project_name == "Radiance Maraikayar Manor":
        sub_project_name = 'Radiance Maraikayar Manor'

    s=Service(constants.engine)
    browser=webdriver.Firefox(service=s)
    
    try:
        browser.get(all_sites.sites[site_name]["url"])
        search=browser.find_element(By.XPATH,'/html/body/div[2]/div/div[2]/section/div[1]/div/div[2]/div/form/fieldset[1]/input')
        search.send_keys(all_sites.sites[site_name]["email"])
        
        passo=browser.find_element(By.XPATH,'/html/body/div[2]/div/div[2]/section/div[1]/div/div[2]/div/form/fieldset[2]/input')
        passo.send_keys(all_sites.sites[site_name]["pass"])
        submit=browser.find_element(By.XPATH,'/html/body/div[2]/div/div[2]/section/div[1]/div/div[2]/div/form/div/button')
        submit.send_keys(Keys.RETURN)

        time.sleep(1)
        #open new tab
        browser.find_element(By.TAG_NAME,'body').send_keys(Keys.COMMAND + 't')
        browser.get(all_sites.sites[site_name]["url2"])
        
        time.sleep(3)
        name=browser.find_element(By.NAME,'lname')
        name.send_keys(name1)

        ## COUNTRY
        country = browser.find_element(By.XPATH, '//*[@id="select2-country-container"]')
        country.click()

        
        country2 = browser.find_element(By.XPATH, '/html/body/span/span/span[1]/input')
        country2.send_keys(country_name)
        country2.send_keys(Keys.RETURN)
        time.sleep(3)

        contact=browser.find_element(By.XPATH,'//*[@id="fmobileNo"]')
        contact.send_keys(phone)
        
        email=browser.find_element(By.NAME,'email')
        email.send_keys(email1)

        project=browser.find_element(By.XPATH,'//*[@id="basic-form-layouts"]/div/div/div/form/div/div[8]/div[3]/span/span[1]/span/span[2]').click()
        project = browser.find_element(By.XPATH,'/html/body/span/span/span[1]/input')
        project.send_keys(sub_project_name)
        project.send_keys(Keys.RETURN)

        
        browser.save_screenshot(save_path1)    
        upload_an_attachment(lead_id, save_path1)
        
        button = browser.find_element(By.XPATH,'//*[@id="basic-form-layouts"]/div/div/div/form/div/center/button/i')
        browser.execute_script("arguments[0].click();", button)

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
