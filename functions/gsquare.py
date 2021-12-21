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

    site_name = "gsquare"
    path = "./" + site_name
    name1 = str(first_name) + ' ' + str(last_name)

    save_paths = getsavePath(path, name1, phone, sub_project_name) 
    save_path1 = save_paths[1]
    save_path = save_paths[0]
    save_path2 = save_paths[2]
    
    
    if sub_project_name == "G Square Sands N Waves":
        sub_project_name = 'G Square Sands N Waves'
    if sub_project_name == "G Square Sunnyvale":
        sub_project_name = 'G Square Sunnyvale'
    if sub_project_name == "G Square Blue Breeze":
        sub_project_name = 'G Square Blue Breeze'
    if sub_project_name == "G Square Seawoods":
        sub_project_name = 'G Square Seawoods'
    if sub_project_name == "G Square Beach Walk":
        sub_project_name = 'G Square Beach Walk'

    '''
    "G Square Sands N Waves", "G Square Sunnyvale", "G Square Blue Breeze", "G Square Seawoods", "G Square Beach Walk"

    '''

    s=Service(constants.engine)

    '''
    all_sites.sites[site_name]["url"]
    all_sites.sites[site_name]["email"]
    all_sites.sites[site_name]["pass"]
    '''

    try:
        browser=webdriver.Firefox(service=s)
        browser.get(all_sites.sites[site_name]["url"])
        name = browser.find_element_by_xpath('/html/body/div/div/div/form/div[2]/div/div/input')
        name.send_keys(name1)
        mail = browser.find_element_by_xpath('/html/body/div/div/div/form/div[3]/div/div/input')
        mail.send_keys(email1)
        phone1 = browser.find_element_by_xpath('/html/body/div/div/div/form/div[4]/div/div/div/input')
        phone1.click()
        phone1.send_keys(phone)
        minbudget = browser.find_element_by_xpath('/html/body/div/div/div/form/div[6]/div[1]/div/select')
        minbudget.click()
        minbudgetvalue = browser.find_element_by_xpath('/html/body/div/div/div/form/div[6]/div[1]/div/select/option[3]')
        minbudgetvalue.click()
        maxbudget = browser.find_element_by_xpath('/html/body/div/div/div/form/div[6]/div[2]/div/select')
        maxbudget.click()
        maxbudgetvalue = browser.find_element_by_xpath('/html/body/div/div/div/form/div[6]/div[2]/div/select/option[11]')
        maxbudgetvalue.click()
        channelpartnername = browser.find_element_by_xpath('/html/body/div/div/div/form/div[7]/div[1]/div/textarea')
        channelpartnername.send_keys(all_sites.sites[site_name]["partner_name"])
        
        
        browser.save_screenshot(save_path1)    
        upload_an_attachment(lead_id, save_path1)

        submit = browser.find_element_by_xpath('/html/body/div/div/div/form/div[9]/div/div/input')
        submit.click()        
        
        browser.save_screenshot(save_path)
        browser.quit()
        upload_an_attachment(lead_id, save_path)
        
        req = 'Success'
        lead = Lead(name=name1, props=sub_project_name, phone=phone,
                    email=email1, status=req, created_at=dt_string, attachments=save_path)
        db.session.add(lead)
        db.session.commit()
        print('Saved but Error Occured' + str(lead.id) + ' ' +
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
