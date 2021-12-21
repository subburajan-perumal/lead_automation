def fin_function(sub_project_name, first_name, last_name, phone, email1):
    from data import all_sites
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.support.ui import Select
    import time
    from full import db, Lead
    from data import constants

    site_name = "alliance"
    path = "./" + site_name
    
    if sub_project_name == "Alliance Humming Gardens":
        sub_project_name = 'Humming Gardens'
    if sub_project_name == "Alliance Humming Gardens":
        sub_project_name = 'Alliance Galleria Residences'

    s=Service(constants.engine)

    '''
    all_sites.sites[site_name]["url"]
    all_sites.sites[site_name]["email"]
    all_sites.sites[site_name]["pass"]
    '''
    
    name1 = str(first_name) + ' ' + str(last_name)

    browser=webdriver.Firefox(service=s)
    browser.get(all_sites.sites[site_name]["url"])
    search=browser.find_element(By.ID,'email')
    search.send_keys(all_sites.sites[site_name]["email"])
    passo=browser.find_element(By.ID,'password')
    passo.send_keys(all_sites.sites[site_name]["pass"])
    submit=browser.find_element(By.ID,'digit_login_signin_submit')
    submit.send_keys(Keys.RETURN)
    
    try:
        time.sleep(10)
        lead=browser.find_elements(By.CLASS_NAME,'kt-menu__item')
        lead[1].click()
    except:
        print('Unknown Error')
        browser.quit()
    time.sleep(5)
    name=browser.find_element(By.NAME,'name')
    name.send_keys(name1)
    contact=browser.find_element(By.NAME,'contact')
    contact.send_keys(phone)
    email=browser.find_element(By.NAME,'email')
    email.send_keys(email1)
    project=Select(browser.find_element(By.ID,'select_project'))
    project.select_by_visible_text(sub_project_name)
    add=browser.find_element(By.ID,'lead_submit_btn').click()

    try:
        aa = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.XPATH,"//*[@id='kt_table_1']/tbody/tr[1]/td[7]"))
        )
        try:
            req=aa.text
            aa.click()
            time.sleep(5)
            browser.save_screenshot(str(path) + '/' + str(name1) + "_" + str(phone) + "_" + str(sub_project_name) + ".png")
            browser.quit()
        except:
            browser.save_screenshot(str(path) + '/' + str(name1) + "_" + str(phone) + "_" + str(sub_project_name) + ".png")
            browser.quit()
    except:
        print('Unknown Error')
        browser.save_screenshot(str(path) + '/' + str(name1) + "_" + str(phone) + "_" + str(sub_project_name) + ".png")
        browser.quit()
        lead = Lead(name=name1, props= sub_project_name, phone = phone, email = email1, status = "Failed")
        db.session.add(lead)
        db.session.commit()
        print('Successfully added \n' + str(lead.name) + ' ' + str(lead.status))
    
    lead = Lead(name=name1, props= sub_project_name, phone = phone, email = email1, status = req)
    db.session.add(lead)
    db.session.commit()
    print('Successfully added' + str(lead.id) + ' ' + str(sub_project_name) + ' ' + str(lead.status))

    return 'Success'