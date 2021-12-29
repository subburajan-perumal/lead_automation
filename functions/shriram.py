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

    site_name = "shriram"
    path = "./" + site_name
    name1 = str(first_name) + ' ' + str(last_name)

    save_paths = getsavePath(path, name1, phone, sub_project_name) 
    save_path1 = save_paths[1]
    save_path = save_paths[0]
    save_path2 = save_paths[2]

    if '+91' in  phone:
        cc='India (+91)'
    elif '+1' in phone:
        cc='Canada (+1)'
    elif '+44' in phone:
        cc='United Kingdom (+44)'
    elif '+93' in phone:
        cc='Afghanistan (+93)'
    elif '+880' in phone:
        cc='Bangladesh (+880)'
    elif '+501' in phone:
        cc='Belize (+501)'
    elif '+55' in phone:
        cc='Brazil (+55)'
    elif '+33' in phone:
        cc='France (+33)'
    elif '+49' in phone:
        cc='Germany (+49)'
    elif '+98' in phone:
        cc='Iran (+98)'
    elif '+39' in phone:
        cc='Italy (+39)'
    elif '+81' in phone:
        cc='Japan (+81)'
    elif '+962' in phone:
        cc='Jordan (+962)'
    elif '+965' in phone:
        cc='Kuwait (+965)'
    elif '+60' in phone:
        cc='Malaysia (+60)'
    elif '+64' in phone:
        cc='New Zealand (+64)'
    elif '+65' in phone:
        cc='Singapore (+65)'
    elif '+34' in phone:
        cc='Spain (+34)'
    elif '+94' in phone:
        cc='Sri Lanka (+94)'
    elif '+971' in phone:
        cc='United Arab Emirates (+971)'
    else:
        print('Failed')

    if sub_project_name == "Shriram Park 63":
        sub_project_name = 'Park 63'
    if sub_project_name == "Shriram Divine City":
        sub_project_name = "Shriram Divine City"
    if sub_project_name == "Shriram Joy":
        sub_project_name = 'Joy@Shriram Temple Bells'
    if sub_project_name == "Shriram Shankari lakeside":
        sub_project_name = 'Lakeside Residences at Shriram Shankari'
    if sub_project_name == "Guduvancher":
        sub_project_name = 'Lakeside Residences at Shriram Shankari'        
    if sub_project_name == "Shriram One City":
        sub_project_name = "Shriram One City - Santrupthi"

    s = Service(constants.engine)
    '''
    all_sites.sites[site_name]["url"]
    all_sites.sites[site_name]["email"]
    all_sites.sites[site_name]["pass"]
    '''
    opts = Options()
    opts.add_argument("--use-fake-ui-for-media-stream")
    browser = webdriver.Firefox(service=s, options=opts)
    browser.get(all_sites.sites[site_name]["url"])

    try:
        agree = browser.find_element(
            By.XPATH, '//*[@id="Rera"]/div/div/div[3]/button').click()
        time.sleep(5)

        radiobox = browser.find_element(By.XPATH, '//*[@id="label_9_24_0"]')
        radiobox.click()
        partner = browser.find_element(
            By.XPATH, '//*[@id="input_9_14_chosen"]/a/span')
        partner.click()
        partner1 = browser.find_element(
            By.XPATH, '//*[@id="input_9_14_chosen"]/div/div/input')
        partner1.send_keys(all_sites.sites[site_name]["channel_partner"])
        partner1.send_keys(Keys.RETURN)
        coustmer_name = browser.find_element(By.XPATH, '//*[@id="input_9_2"]')
        coustmer_name.send_keys(name1)
        coustmer_email = browser.find_element(By.XPATH, '//*[@id="input_9_3"]')
        coustmer_email.send_keys(email1)
        code = Select(browser.find_element(By.XPATH, '//*[@id="input_9_56"]'))
        code.select_by_visible_text(cc)
        coustmer_phone = browser.find_element(By.XPATH, '//*[@id="input_9_4"]')
        coustmer_phone.send_keys(phone)
        resident = Select(browser.find_element(
            By.XPATH, '//*[@id="input_9_57"]'))
        resident.select_by_visible_text('Local')
        coustmer_city = browser.find_element(By.XPATH, '//*[@id="input_9_58"]')
        coustmer_city.send_keys('Chennai')
        project_city = Select(browser.find_element(
            By.XPATH, '//*[@id="input_9_6"]'))
        project_city.select_by_visible_text('Chennai')
        time.sleep(3)
        area = Select(browser.find_element(By.XPATH, '//*[@id="input_9_16"]'))
        area.select_by_visible_text(sub_project_name)
        comment = browser.find_element(By.XPATH, '//*[@id="input_9_12"]')
        comment.send_keys('Nil')
        email10 = browser.find_element(By.XPATH, '//*[@id="input_9_47"]')
        email10.send_keys(all_sites.sites[site_name]["email"])
        phone10 = browser.find_element(By.XPATH, '//*[@id="input_9_48"]')
        phone10.send_keys(all_sites.sites[site_name]["mobile"])
        
        
        browser.save_screenshot(save_path1)    
        upload_an_attachment(lead_id, save_path1)
        
        submit = browser.find_element(
            By.XPATH, '//*[@id="gform_submit_button_9"]')
        submit.click()
        time.sleep(20)

        aa = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//*[@id='gform_9']/div[1]"))
        )
        
        print('error')
        browser.save_screenshot(save_path)
        browser.quit()
        upload_an_attachment(lead_id, save_path)
        
        
        req = 'Success'
        lead = Lead(name=name1, props=sub_project_name, phone=phone,
                    email=email1, status=req, created_at=dt_string, attachments=save_path1)
        db.session.add(lead)
        db.session.commit()
        print('Successfully added ' + str(lead.id) + ' ' +
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
