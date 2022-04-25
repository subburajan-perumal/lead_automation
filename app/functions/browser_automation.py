import phonenumbers
from selenium.webdriver import Firefox 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.alert import Alert
from app.util.utility import getName
import phonenumbers as PN
from celery.utils.log import get_task_logger
from phonenumbers import geocoder as GC
import logging
import time
# browserLog=logging.getLogger("browser_log")
browserLog=get_task_logger(__name__)
# browserLog.set



def adityaram(subproject:str, browser:Firefox, site_data:dict, lead_data:dict, path:list) :
    try:
        browserLog.info(f"Site: {site_data['name']}, Project:{subproject}")
        save_path= path

        browser.get(site_data["url"])
        #client name
        
        #client name
        name=browser.find_elements(By.XPATH,'/html/body/div[1]/div/div/div/div/div/div/form/div[2]/div/div/input[1]')
        name[0].send_keys(lead_data['name'])
        #client email
        email=browser.find_elements(By.XPATH,'/html/body/div[1]/div/div/div/div/div/div/form/div[3]/div/div/input')
        email[0].send_keys(lead_data['email'])
        #client contact
        contact=browser.find_elements(By.XPATH,'/html/body/div[1]/div/div/div/div/div/div/form/div[4]/div/div/div/input')
        contact[0].send_keys(lead_data['phone'])
        #CPname
        cpname1=Select(browser.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div/div/div/form/div[5]/div[1]/div/select'))
        cpname1.select_by_visible_text(site_data["cpname"])
        #CPphone
        cpphn1=browser.find_elements(By.XPATH,'/html/body/div[1]/div/div/div/div/div/div/form/div[5]/div[2]/div/input')
        cpphn1[0].send_keys(site_data["cpphn"])
        #Project
        proj1=Select(browser.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div/div/div/form/div[6]/div/div/select'))
        proj1.select_by_visible_text(subproject)
        time.sleep(3)
        browser.save_screenshot(save_path[0])

        add=browser.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div/div/div/form/div[8]/div/div/input').click()
        time.sleep(3)

        browser.save_screenshot(save_path[1])    
        browser.close()
        browserLog.info("adityaram finised")
        return 1
    except Exception as e:
        # print(str(e))
        browserLog.exception(f"Site:{site_data['name']}")
        browser.save_screenshot(save_path[2])
        return -1

#working
def akshaya(subproject:str, browser:Firefox, site_data:dict, lead_data:dict,automate_path:list):
    try:
        browserLog.info(f"Site: {site_data['name']}, Project:{subproject}")
        save_path = automate_path
        fullname=str(lead_data['name'])
        first_name,last_name=getName(fullname)
        browser.get(site_data["url"])
        fl_email = browser.find_element(By.ID, "user_email")
        fl_email.send_keys(site_data["email"])
        fl_password = browser.find_element(By.ID, "user_password")
        fl_password.send_keys(site_data["pass"])
        browser.find_element(By.XPATH, "//button[@type='submit']").click()
        f_Leads = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, "Leads")))
        # f_Leads = browser.find_element(By.LINK_TEXT, "Leads")
        f_Leads.click()
        f_addlead = browser.find_element(
            By.XPATH, "//a[@href='/broker/2150/leads/new']")
        f_addlead.click()
        f_firstname = browser.find_element(By.ID, "lead_first_name")
        f_firstname.send_keys(first_name)
        f_lastname = browser.find_element(By.ID, "lead_last_name")
        f_lastname.send_keys(last_name)
        f_mail = browser.find_element(
                                    By.XPATH, 
                                    '/html/body/div[1]/div/div[2]/form/div[2]/div[2]/div[2]/div[1]/div/div/a'
                                    )
        f_mail.click()
        f_mail1 = browser.find_element(By.XPATH, '/html/body/div[3]/div/input')
        f_mail1.click()
        f_mail1.send_keys(lead_data.get("email"))
        f_mail1.send_keys(Keys.RETURN)
        f_phone = browser.find_element(By.XPATH, '//*[@id="lead_phone"]')
        f_phone.click()
        f_phone.send_keys(lead_data.get("phone"))
        f_button2 = browser.find_element(
            By.XPATH, '//*[@id="s2id_lead_project_ids"]/a/span[2]')
        f_button2.click()
        f_project1 = browser.find_element(
            By.XPATH, '/html/body/div[4]/div/input')
        f_project1.send_keys(subproject)
        f_project1.send_keys(Keys.RETURN)

        browser.save_screenshot(save_path[0])
        f_save = browser.find_element(By.XPATH, '//*[@id="new_lead"]/div[6]/input')
        f_save.click()
        browser.implicitly_wait(5)
        browser.save_screenshot(save_path[1])
        browser.close()
        return 1

    except Exception as e:
        browserLog.exception(f"Site:{site_data['name']}")
        # print(str(e))
        browser.save_screenshot(save_path[2])
        browser.close()
        return -1

#issue in handling subproject
def alliance(subproject:str, browser:Firefox, site_data:dict, lead_data:dict, automate_path:list):
    try:
        subproject_2=""
        # Villabelvedere/Eternity
        if subproject=="Villabelvedere":
            subproject="Villabelvedere/Eternity"
            subproject_2="Villabelvedere"
        
        if subproject=="Urbanrise Eternity":
            subproject="Villabelvedere/Eternity"
            subproject_2="Urbanrise Eternity"
        
        # OMR Cluster - JS/CNCB,CNGS
        if subproject=="Codename Chennai's Best":
            subproject="OMR Cluster - JS/CNCB,CNGS"
            subproject_2="Codename Chennai's Best"

        if subproject=="Codename Gold Standard":
            subproject="OMR Cluster - JS/CNCB,CNGS"
            subproject_2="Codename Gold Standard"
        
        if subproject=="Jasmine springs":
            subproject="OMR Cluster - JS/CNCB,CNGS"
            subproject_2="Jasmine springs"


        save_path = automate_path
        fullname=str(lead_data['name'])
        phone=PN.parse(lead_data["phone"])
        phoneno=PN.format_number(phone,PN.PhoneNumberFormat.E164)
        #testting
        first_name,last_name=lead_data['first_name'],lead_data['last_name']
        browser.get(site_data["url"])
        fl_search=browser.find_element(By.ID,'email')
        fl_search.send_keys(site_data["email"])
        fl_passo=browser.find_element(By.ID,'password')
        fl_passo.send_keys(site_data["pass"])
        fs_submit=browser.find_element(By.ID,'digit_login_signin_submit')
        fs_submit.send_keys(Keys.RETURN)
        time.sleep(10)
        f_lead=browser.find_elements(By.CLASS_NAME,'kt-menu__item')
        f_lead[1].click()
        time.sleep(5)
        f_name=browser.find_element(By.NAME,'name')
        f_name.send_keys(lead_data['name'])
        contact=browser.find_element(By.NAME,'contact')
        contact.send_keys(phoneno)
        contact.clear()
        contact.send_keys(phone.national_number)
        email=browser.find_element(By.NAME,'email')
        email.send_keys(lead_data['email'])
        project=Select(browser.find_element(By.ID,'select_project'))
        project.select_by_visible_text(subproject)
        if subproject_2 != "" :
            projectsub=Select(browser.find_element(By.ID,'sub_project_select'))
            projectsub.select_by_visible_text(subproject_2)


        # browser.save_screenshot(save_path[0])    

        add=browser.find_element(By.ID,'lead_submit_btn').click()
        aa = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.XPATH,"//*[@id='kt_table_1']/tbody/tr[1]/td[7]"))
        )
        # browser.save_screenshot(save_path[0])
        aa.click()
        
        time.sleep(3) ## FOR CHANGING WAIT TIME
        browser.save_screenshot(save_path[1])
        browser.close()
        return 1

    except Exception as e:
        browserLog.exception(f"Site:{site_data['name']}")
        browser.save_screenshot(save_path[2])
        return -1
#working
def brigade(subproject:str, browser: Firefox, site_data:dict, lead_data:dict,automate_path:list):         
    try:    
        browserLog.info(f"Site: {site_data['name']}, Project:{subproject}")
        save_path = automate_path
        fullname= str(lead_data['name'])
        first_name, last_name = getName(fullname)
        
    #browser# yield "on working"
        save_path= automate_path
        browser.get(site_data["url"])
        company_name = browser.find_element(By.XPATH, '//*[@id="input_5"]')
        company_name.send_keys(site_data["company"])
        #agent name
        f_agentf = browser.find_elements(By.XPATH, '//*[@id="first_6"]')
        f_agentf[0].send_keys(site_data["agentf1"])
        f_agentl = browser.find_elements(By.XPATH, '//*[@id="last_6"]')
        f_agentl[0].send_keys(site_data["agentl1"])
        
        #agent mobile number
        f_aph11 = browser.find_elements(By.XPATH, '//*[@id="input_7_country"]')
        f_aph11[0].send_keys(site_data["aph1"])
        f_aph21 = browser.find_elements(By.XPATH, '//*[@id="input_7_area"]')
        f_aph21[0].send_keys(site_data["aph2"])
        f_aph31 = browser.find_elements(By.XPATH, '//*[@id="input_7_phone"]')
        f_aph31[0].send_keys(site_data["aph3"])
        
        #agent email
        f_mail = browser.find_elements(By.XPATH, '//*[@id="input_8"]')
        f_mail[0].send_keys(site_data["email"])
        
        #client name
        f_firstname= browser.find_element(By.XPATH, '//*[@id="first_11"]')
        f_firstname.send_keys(first_name)
        f_lastname= browser.find_element(By.ID, 'last_11')
        f_lastname.send_keys(last_name)
        
        #mobile number 1
        f_aph1c = browser.find_element(By.XPATH, '//*[@id="input_12_country"]')
        f_aph1c.send_keys(site_data["aph1"])
        f_aph2c = browser.find_element(By.XPATH, '//*[@id="input_12_area"]')
        f_aph2c.send_keys(site_data["aph2"])
        f_aph3c = browser.find_element(By.XPATH, '//*[@id="input_12_phone"]')
        f_aph3c.send_keys(lead_data["phone"])
        
        #mobile number 2
        f_aph1c2 = browser.find_element(By.XPATH, '//*[@id="input_14_country"]')
        f_aph1c2.send_keys(site_data["aph1"])
        f_aph2c2 = browser.find_element(By.XPATH, '//*[@id="input_14_area"]')
        f_aph2c2.send_keys(site_data["aph2"])
        f_aph3c2 = browser.find_element(By.XPATH, '//*[@id="input_14_phone"]')
        f_aph3c2.send_keys(lead_data["phone"])
        
        #emails
        f_email11= browser.find_element(By.XPATH, '//*[@id="input_13"]')
        f_email11.send_keys(lead_data["email"])
        f_email21= browser.find_element(By.XPATH, '//*[@id="input_15"]')
        f_email21.send_keys(lead_data["email"])
        
        #project name
        project=Select(browser.find_element(By.XPATH, '//*[@id="input_16"]'))
        project.select_by_visible_text(subproject)

        browser.save_screenshot(save_path[0])    

        f_add=browser.find_element(By.XPATH,'//*[@id="input_2"]').click()
        browser.implicitly_wait(5)
        # time.sleep(10)
        browser.save_screenshot(save_path[1])
        browser.close()
        print("brigage website work successfully")
        return 1

    except Exception as e:
        browserLog.exception(f"Site:{site_data['name']}")
        browser.save_screenshot(save_path[2])
        return -1

#working
def casagrand(subproject, browser, site_data, lead_data, automate_path):
    try:
        browserLog.info(f"Site: {site_data['name']}, Project:{subproject}")
        save_path = automate_path
        fullname=str(lead_data['name'])
        first_name,last_name=getName(fullname)
        browser.get(site_data["url"])
        fl_email = browser.find_element(By.ID, "user_email")
        fl_email.send_keys(site_data["email"])
        fl_password = browser.find_element(By.ID,"user_password")
        fl_password.send_keys(site_data["pass"])
        browser.find_element(By.XPATH,"//button[@type='submit']").click()

        Leads = browser.find_element(By.LINK_TEXT, "Leads")
        Leads.click()
        addlead = browser.find_element(By.XPATH, "/html/body/div/div/div[1]/div/ul/li/ul/li[2]/a")
        addlead.click()

        firstname = browser.find_element(By.ID, "lead_first_name")
        firstname.send_keys(fullname)
        lastname = browser.find_element(By.ID, "lead_last_name")
        lastname.send_keys(fullname)

        #nri = browser.find_element(By.ID, "lead_nri")
        #nri.click()
        #nri.click()

        f_mail = browser.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/form/div[2]/div[2]/div[2]/div[1]/div/div/a')
        f_mail.click()
        f_alt_mail = browser.find_element(By.XPATH, '/html/body/div[3]/div/input')
        f_alt_mail.click()
        f_alt_mail.send_keys(lead_data['email'])
        f_alt_mail.send_keys(Keys.RETURN)
        f_phone = browser.find_element(By.XPATH, '//*[@id="lead_phone"]')
        f_phone.click()
        f_phone.send_keys(lead_data['phone'])
        button2 = browser.find_element(By.XPATH, '//*[@id="s2id_lead_project_ids"]/a/span[2]')
        button2.click()
        f_project = browser.find_element(By.XPATH, '/html/body/div[4]/div/input')
        f_project.send_keys(subproject)
        f_project.send_keys(Keys.RETURN)

        browser.save_screenshot(save_path[0])    
    

        fs_save = browser.find_element(By.XPATH, '//*[@id="new_lead"]/div[6]/input')
        fs_save.click()
        
        time.sleep(5)
        browser.save_screenshot(save_path[1])
        browser.close()
        return 1
    except Exception as e:
        browserLog.exception(f"Site:{site_data['name']}")
        browser.save_screenshot(save_path[2])
        return -1


def doshi(subproject, browser, site_data, lead_data, path):
    try:
        browserLog.info(f"Site: {site_data['name']}, Project:{subproject}")
        save_path = path
        browser.get(site_data["url"])
        search=browser.find_element(By.ID,'username')
        search.send_keys(site_data["email"])
        passo=browser.find_element(By.ID,'password')
        passo.send_keys(site_data["pass"])
        submit=browser.find_element(By.NAME,'user_login').click()
        time.sleep(2)
        lead=browser.find_elements(By.CLASS_NAME,'icon-plus')[0].click()
        time.sleep(2)
        name  = browser.find_element(By.NAME, "leads_name")
        name.send_keys(lead_data['name'])
        contact=browser.find_element(By.NAME,'leads_mobile_number')
        contact.send_keys(lead_data['phone'])
        email=browser.find_element(By.NAME,'leads_email')
        email.send_keys(lead_data['email'])

        tem = browser.find_element(By.XPATH, '/html/body/div[7]/div/div/div/form/div[2]/div[3]/div[3]/select')
        sct = Select(tem)
        sct.select_by_visible_text(subproject)

        browser.save_screenshot(save_path[0])
        browser.implicitly_wait(5)
        add=browser.find_element(By.NAME,'leads_add').click()
        browser.save_screenshot(save_path[1])
        browser.close()
        return 1

    except Exception as e:
        browserLog.exception(f"Site:{site_data['name']}")
        browser.save_screenshot(save_path[2])
        return -1

#onworking
def dlf(subproject:str, browser:Firefox, site_data:dict, lead_data:dict, path:list):
    
    try:
        browserLog.info(f"Site: {site_data['name']}, Project:{subproject}")
        save_path=path
        locationname="Siruseri"
        phone=PN.parse(lead_data['phone'])
        phoneno=phone.national_number
        countrycode="+"+str(phone.country_code)
        
        browser.get(site_data["url"])
        search=browser.find_element(By.XPATH,'/html/body/div/div/div/form/div[2]/input')        
        search.send_keys(site_data["email"])
        
        time.sleep(1)
        pwdd=browser.find_element(By.XPATH,'/html/body/div/div/div/form/div[3]/input')
        pwdd.send_keys(site_data["pass"])
        time.sleep(1)        
        submit=browser.find_element(By.XPATH,'/html/body/div/div/div/form/div[4]/button')
        submit.send_keys(Keys.RETURN)

        time.sleep(5)
        browser.get(site_data["url2"])

        
        
        namelead=browser.find_element(By.XPATH,'/html/body/div[2]/div/div/form/div[1]/div[1]/input')
        namelead.send_keys(lead_data['name'])
        time.sleep(1)

        projectlocation=browser.find_element(By.XPATH,'//*[@id="location"]')
        projectlocation.send_keys(locationname)        
        projectlocation.send_keys(Keys.RETURN)


        emaillead=browser.find_element(By.XPATH,'//*[@id="email"]')
        emaillead.send_keys(lead_data['email'])
        time.sleep(1)        


        remarks=browser.find_element(By.XPATH,'//*[@id="remarks"]')
        remarks.send_keys(subproject)
        time.sleep(1)

        country2 = browser.find_element(By.XPATH, '//*[@id="country_code"]')
        country2.click()
        time.sleep(1)        
        country2.send_keys(countrycode)
        time.sleep(1)        
        country2.send_keys(Keys.RETURN)
        time.sleep(1)

        contact=browser.find_element(By.XPATH,'/html/body/div[2]/div/div/form/div[2]/div[2]/input')
        contact.send_keys(phoneno)
        time.sleep(1)


        browser.save_screenshot(save_path[0])
        submitbutton = browser.find_element(By.XPATH,'//*[@id="submit"]')
        submitbutton.click()
        
        time.sleep(10)
        browser.save_screenshot(save_path[1])
        browser.close()
        return 1        
    
    except Exception as e:
        browserLog.exception(f"Site:{site_data['name']}")
        browser.save_screenshot(save_path[2])
        return -1

#working
def dra(subproject, browser, site_data, lead_data, path):
    try:
        browserLog.info(f"Site: {site_data['name']}, Project:{subproject}")
        save_path=path

        browser.get(site_data["url"])
        email = browser.find_element(By.ID, "user_email")
        email.send_keys(site_data["email"])
        password = browser.find_element(By.ID,"user_password")
        password.send_keys(site_data["pass"])
        browser.find_element(By.XPATH,"//button[@type='submit']").click()

        Leads = browser.find_element(By.LINK_TEXT, "Leads")
        Leads.click()
        addlead = browser.find_element(By.XPATH, "/html/body/div/div/div[1]/div/ul/li/ul/li[2]/a")
        addlead.click()

        firstname = browser.find_element(By.ID, "lead_first_name")
        firstname.send_keys(lead_data['name'])
        lastname = browser.find_element(By.ID, "lead_last_name")
        lastname.send_keys(lead_data['name'])

        #nri = browser.find_element(By.ID, "lead_nri")
        #nri.click()
        #nri.click()

        mail = browser.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/form/div[2]/div[2]/div[2]/div[1]/div/div/a')
        mail.click()
        mail1 = browser.find_element(By.XPATH, '/html/body/div[3]/div/input')
        mail1.click()
        mail1.send_keys(lead_data['email'])
        mail1.send_keys(Keys.RETURN)
        phone1 = browser.find_element(By.XPATH, '//*[@id="lead_phone"]')
        phone1.click()
        phone1.send_keys(lead_data.get("phone"))
        button2 = browser.find_element(By.XPATH, '//*[@id="s2id_lead_project_ids"]/a/span[2]')
        button2.click()
        project = browser.find_element(By.XPATH, '/html/body/div[4]/div/input')
        project.send_keys(subproject)
        project.send_keys(Keys.RETURN)


        browser.save_screenshot(save_path[0])
        save = browser.find_element(By.XPATH, '//*[@id="new_lead"]/div[6]/input')
        save.click()

        browser.implicitly_wait(5)
        browser.save_screenshot(save_path[1])
        browser.close()
        return 1

    except Exception as e:
        browserLog.exception(f"Site:{site_data['name']}")
        browser.save_screenshot(save_path[2])
        return -1

#error occur at the end of selenium
def fomra(subproject:str, browser, site_data:dict, lead_data:dict, automate_path:list):
    try:
        browserLog.info(f"Site: {site_data['name']}, Project:{subproject}")
        save_path = automate_path
        fullname= str(lead_data['name'])
        first_name, last_name = getName(fullname)
        browser.get(site_data['url'])
        f_name= browser.find_element(By.XPATH, '/html/body/div/div/div/div/div/div/div/form/div[2]/div/div/input[1]')
        f_name.send_keys(fullname)
        f_email= browser.find_element(By.XPATH, '/html/body/div/div/div/div/div/div/div/form/div[3]/div/div/input')
        f_email.send_keys(lead_data['email'])
        f_phone= browser.find_element(By.XPATH, '//html/body/div/div/div/div/div/div/div/form/div[4]/div/div/div/input')
        f_phone.send_keys(lead_data['phone'])
        f_project= Select(browser.find_element(By.XPATH, '/html/body/div/div/div/div/div/div/div/form/div[7]/div/div/select'))
        f_project.select_by_visible_text(site_data["partner_name"])
        
        f_channel_pn= Select(browser.find_element(By.XPATH, '/html/body/div/div/div/div/div/div/div/form/div[5]/div/div/select'))
        f_channel_pn.select_by_visible_text(subproject)
        
        f_channel_phone= browser.find_element(By.XPATH, '/html/body/div/div/div/div/div/div/div/form/div[8]/div/div/input')
        f_channel_phone.send_keys(site_data["channel_phone_number"])

        
        browser.save_screenshot(save_path[0])    
    

        f_submit= browser.find_element(By.XPATH, '/html/body/div/div/div/div/div/div/div/form/div[9]/div/div/input').click()
        time.sleep(5)
        # browser.implicitly_wait(5)

        
        browser.save_screenshot(save_path[1])
        browser.close()
        return 1
    except Exception as e:
        browserLog.exception(f"Site:{site_data['name']}")
        browser.save_screenshot(save_path[2])
        browser.close()
        return -1


def gsquare(subproject, browser, site_data, lead_data, path):
    try:
        browserLog.info(f"Site: {site_data['name']}, Project:{subproject}")
        save_path=path

        browser.get(site_data["url"])
        name = browser.find_element_by_xpath('/html/body/div/div/div/form/div[2]/div/div/input')
        name.send_keys(lead_data['name'])
        mail = browser.find_element_by_xpath('/html/body/div/div/div/form/div[3]/div/div/input')
        mail.send_keys(lead_data['email'])
        phone1 = browser.find_element_by_xpath('/html/body/div/div/div/form/div[4]/div/div/div/input')
        phone1.click()
        phone1.send_keys(lead_data['phone'])
        minbudget = browser.find_element_by_xpath('/html/body/div/div/div/form/div[6]/div[1]/div/select')
        minbudget.click()
        minbudgetvalue = browser.find_element_by_xpath('/html/body/div/div/div/form/div[6]/div[1]/div/select/option[3]')
        minbudgetvalue.click()
        maxbudget = browser.find_element_by_xpath('/html/body/div/div/div/form/div[6]/div[2]/div/select')
        maxbudget.click()
        maxbudgetvalue = browser.find_element_by_xpath('/html/body/div/div/div/form/div[6]/div[2]/div/select/option[11]')
        maxbudgetvalue.click()
        channelpartnername = browser.find_element_by_xpath('/html/body/div/div/div/form/div[7]/div[1]/div/textarea')
        channelpartnername.get(site_data["partner_name"])

        browser.save_screenshot(save_path[0])
        browser.implicitly_wait(5)
        browser.save_screenshot(save_path[1])
        browser.close()
        return 1

    except Exception as e:
        browserLog.exception(f"Site:{site_data['name']}")
        browser.save_screenshot(save_path[2])
        return -1

#working
def hiranandani(subproject, browser, site_data, lead_data, path):
    try:
        browserLog.info(f"Site: {site_data['name']}, Project:{subproject}")
        save_path=path
        phone=PN.parse(lead_data['phone'])
        browser.get(site_data["url"])
        tem = browser.find_element(By.CLASS_NAME, 'reffer-btn').click()

        name  = browser.find_element(By.NAME, "Pname")
        name.send_keys(lead_data['name'])

        contact=browser.find_element(By.NAME,'pmob')
        contact.send_keys(phone.national_number)

        intrest_project = browser.find_element(By.NAME, 'interested')
        new = Select(intrest_project)
        new.select_by_index(2)

        email=browser.find_element(By.NAME,'pemail')
        email.send_keys(lead_data['email'])

        add=browser.find_element(By.XPATH,'/html/body/div[3]/div/div/div/form/div[1]/div/div/div[6]/div/div[2]/span/span').click()

        intrest_project = browser.find_element(By.NAME, 'cname')
        new = Select(intrest_project)
        new.select_by_index(3)      

        browser.save_screenshot(save_path[0])
        add=browser.find_element(By.XPATH,'/html/body/div[3]/div/div/div/form/button').click()

        browser.implicitly_wait(5)
        browser.save_screenshot(save_path[1])
        browser.close()
        return 1

    except Exception as e:
        browserLog.exception(f"Site:{site_data['name']}")
        browser.save_screenshot(save_path[2])
        return -1

#working
def krishnagrp(subproject, browser, site_data, lead_data, path):
    try:
        browserLog.info(f"Site: {site_data['name']}, Project:{subproject}")
        save_path=path

        browser.get(site_data["url"])
        name = browser.find_element_by_xpath('//*[@id="tab-one"]/div/div[2]/div/div/div/form/div[2]/div/div/input ')
        name.send_keys(lead_data['name'])
        # Email id
        mail = browser.find_element_by_xpath('//*[@id="tab-one"]/div/div[2]/div/div/div/form/div[3]/div/div/input')
        mail.send_keys(lead_data['email'])
        # Project Dropdown
        project = browser.find_element_by_xpath('//*[@id="tab-one"]/div/div[2]/div/div/div/form/div[5]/div/div/select')
        project.click()
        # Phone Number
        phone = browser.find_element_by_xpath('//*[@id="tab-one"]/div/div[2]/div/div/div/form/div[4]/div/div/div/input')
        phone.send_keys(lead_data['phone'])
        # Channel Parter
        channelname = browser.find_element_by_xpath('//*[@id="tab-one"]/div/div[2]/div/div/div/form/div[7]/div/div/select')
        channelname.click()

        cpname=browser.find_element_by_xpath('/html/body/section/div/div/div[2]/div/div/div/div[2]/div/div/div/form/div[7]/div/div/select/option[32]')
        cpname.click()
        time.sleep(1)                        
        
        browser.save_screenshot(save_path[0])
        
        submit = browser.find_element_by_xpath('/html/body/section/div/div/div[2]/div/div/div/div[2]/div/div/div/form/div[9]/div/div/ input')
        submit.click()


        browser.implicitly_wait(5)
        browser.save_screenshot(save_path[1])
        browser.close()
        return 1

    except Exception as e:
        browserLog.exception(f"Site:{site_data['name']}")
        browser.save_screenshot(save_path[2])
        
        return -1

#working
def lancor(subproject:str, browser:Firefox, site_data:dict, lead_data: dict, path:list):
    try:
        browserLog.info(f"Site: {site_data['name']}, Project:{subproject}")
        save_path = path
        first_name,last_name= getName(lead_data['name'])
        browser.get(site_data["url"])
        email = browser.find_element(By.ID, "user_email")
        email.send_keys(site_data["email"])
        password = browser.find_element(By.ID,"user_password")
        password.send_keys(site_data["pass"])
        browser.find_element(By.XPATH,"//button[@type='submit']").click()

        Leads = browser.find_element(By.LINK_TEXT, "Leads")
        Leads.click()
        addlead = browser.find_element(By.XPATH, "//a[@href='/broker/1893/leads/new']")
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
        mail1.send_keys(lead_data['email'])
        mail1.send_keys(Keys.RETURN)
        phone1 = browser.find_element(By.XPATH, '//*[@id="lead_phone"]')
        phone1.click()
        phone1.send_keys(lead_data['phone'])
        button2 = browser.find_element(By.XPATH, '//*[@id="s2id_lead_project_ids"]/a/span[2]')
        button2.click()
        project = browser.find_element(By.XPATH, '/html/body/div[4]/div/input')
        project.send_keys(subproject)
        project.send_keys(Keys.RETURN)
        browser.save_screenshot(save_path[0])

        save = browser.find_element(By.XPATH, '//*[@id="new_lead"]/div[6]/input')
        save.click()
        
        time.sleep(5)
        browser.save_screenshot(save_path[1])

        return 1

    except Exception as e:
        browserLog.exception(f"Site:{site_data['name']}")
        browser.save_screenshot(save_path[2])
        return -1

#working
def lifestyle(subproject:str, browser:Firefox, site_data:dict, lead_data:dict, path:list):
    
    #location = 'A'
    #budget = 'Below 5'
    #enquiry_Medium = 'Server Call'
    #channel_partner = 'LeadAutomation'
    
    # save_paths = getsavePath(path, name1, phone, sub_project_name) 
    # save_path1 = save_paths[1]
    # save_path = save_paths[0]
    # save_path2 = save_paths[2]



    try:
        browserLog.info(f"Site: {site_data['name']}, Project:{subproject}")
        save_path=path

        phone=PN.parse(lead_data['phone'])
        phone_no = phone.national_number
        alternet_contact = phone.national_number
        whatsapp = phone.national_number
        remark = "NIL"
        project_intrested = subproject
        #flat_type = '1 BHK'
        enquiry_sourse = 'Channel Partner'
        enquiry_owner  = 'LeadAutomation'
        browser.get(site_data["url"])
        search=browser.find_element(By.ID,'username')
        search.send_keys(site_data["email"])
        passo=browser.find_element(By.ID,'password')
        passo.send_keys(site_data["pass"])
        submit=browser.find_element(By.CLASS_NAME,'signin-button').click()

        #submit.send_keys(Keys.RETURN)
        time.sleep(2)
        lead=browser.find_elements(By.ID,'menubar_item_Appointments')[1].click()
        time.sleep(2)

        adding=browser.find_element(By.CLASS_NAME,'icon-plus')
        adding.click()
        time.sleep(2)
        name  = browser.find_element(By.NAME, "contactname")
        name.send_keys(lead_data["name"])
        contact=browser.find_element(By.NAME,'mobile')
        contact.send_keys(phone_no)

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
        email.send_keys(lead_data["email"])

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
        new.send_keys(site_data["channel_partner"])
        new.send_keys(Keys.RETURN)

        #project=Select(browser.find_element(By.XPATH,'//*[@id="Appointments_editView_fieldName_description"]'))
        #project.select_by_visible_text(remark)
        
        
        # browser.save_screenshot(save_path1)    
        # upload_an_attachment(lead_id, save_path1)
        browser.save_screenshot(save_path[0])
        add=browser.find_element(By.XPATH,"/html/body/div[2]/div[3]/div/div[2]/div[2]/form/div[1]/span/button").click()
        time.sleep(7)
        browser.save_screenshot(save_path[1])

        # browser.save_screenshot(save_path)    
        # browser.quit()
        # upload_an_attachment(lead_id, save_path)
        
        return 1
        # lead = Lead(name=name1, props= sub_project_name, phone = phone, email = email1, status = req, created_at =  dt_string, attachments = save_path)
        # db.session.add(lead)
        # db.session.commit()
        # print('Successfully added' + str(lead.id) + ' ' + str(sub_project_name) + ' ' + str(lead.status))
    
    except Exception as e:
        browserLog.exception(f"Site:{site_data['name']}")
        browser.save_screenshot(save_path[2])

        # browser.save_screenshot(save_path2)
        # browser.quit()
        return -1

#working
def pragnya(subproject, browser, site_data, lead_data, path):
    try:
        browserLog.info(f"Site: {site_data['name']}, Project:{subproject}")
        save_path=path

        browser.get(site_data["url"])

        name  = browser.find_element(By.XPATH, '/html/body/section[3]/div/div/div[2]/div/form/input[1]')
        name.send_keys(site_data['partner'])

        name  = browser.find_element(By.XPATH, '/html/body/section[3]/div/div/div[2]/div/form/input[2]')
        name.send_keys(lead_data['name'])

        #intrest_project = browser.find_element(By.ID, 'leads_project')

        email=browser.find_element(By.XPATH,'/html/body/section[3]/div/div/div[2]/div/form/input[3]')
        email.send_keys(lead_data['email'])

        contact=browser.find_element(By.XPATH,'/html/body/section[3]/div/div/div[2]/div/form/input[4]')
        contact.send_keys(lead_data['phone'])

        try:
            block = browser.find_element(By.XPATH, '//*[@id="cn-accept-cookie"]')
            block.click()
        except:
            pass

        browser.save_screenshot(save_path[0])
        add=browser.find_element(By.XPATH,'/html/body/section[3]/div/div/div[2]/div/form/input[6]')
        add.click()

        browser.implicitly_wait(5)
        browser.save_screenshot(save_path[1])
        browser.close()
        return 1

    except Exception as e:
        browserLog.exception(f"Site:{site_data['name']}")
        browser.save_screenshot(save_path[2])
    
        return -1

#working
def radiance(subproject, browser, site_data, lead_data, path):
    try:
        browserLog.info(f"Site: {site_data['name']}, Project:{subproject}")
        save_path= path
        phone_no= PN.parse(lead_data['phone'])
        country_name=GC.country_name_for_number(phone_no,'en')
        # country_code=phone_no.country_code
        fv_phoneNo=phone_no.national_number
        browser.get(site_data["url"])

        fl_username= browser.find_element(By.XPATH, '/html/body/div[2]/div/div[2]/section/div[1]/div/div[2]/div/form/fieldset[1]/input')
        fl_username.send_keys(site_data["email"])
        
        fl_password= browser.find_element(By.XPATH, '/html/body/div[2]/div/div[2]/section/div[1]/div/div[2]/div/form/fieldset[2]/input')
        fl_password.send_keys(site_data["pass"])
        fl_submit= browser.find_element(By.XPATH, '/html/body/div[2]/div/div[2]/section/div[1]/div/div[2]/div/form/div/button')
        fl_submit.send_keys(Keys.RETURN)

        time.sleep(1)
        #open new tab
        browser.find_element(By.TAG_NAME,'body').send_keys(Keys.COMMAND + 't')
        browser.get(site_data["url2"])
        
        time.sleep(2)
        f_name=browser.find_element(By.NAME, 'lname')
        f_name.send_keys(lead_data['name'])

        ## COUNTRY
        f_country = browser.find_element(By.XPATH, '//*[@id="select2-country-container"]')
        if str(f_country.text).lower()!=country_name.lower():
            print(country_name)
            f_country.click()
            f_country2 = browser.find_element(By.XPATH, '/html/body/div[4]/div/div[2]/section/div/div/div/form/div/div[2]/div[3]/span/span[1]/span/span[2]')
            f_country3= browser.find_element(By.XPATH,"/html/body/span/span/span[1]/input")
            f_country3.send_keys(country_name)
            f_selectcountry=browser.find_element(By.XPATH,'//li[contains(@id,"select2-country-result-")]')
            f_selectcountry.click()
            contact=browser.find_element(By.XPATH, '//*[@id="fmobileNo"]')
            
        else:
            contact=browser.find_element(By.XPATH, '//*[@id="mobileNo"]')
        
        contact.send_keys(fv_phoneNo)
        
        email= browser.find_element(By.ID, 'emailId')
        email.send_keys(lead_data['email'])
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
    
        project= browser.find_element(By.XPATH, '/html/body/div[4]/div/div[2]/section/div/div/div/form/div/div[8]/div[3]/span/span[1]/span/span[2]')
        project.click()
        search_project= browser.find_element(By.XPATH, '/html/body/span/span/span[1]/input')
        search_project.send_keys(subproject)
        # project_list= 
        project_list=browser.find_element(By.XPATH,'//li[contains(@id,"select2-interestedproject-" )]')
        project_list.click()
        
        # fs_button=browser.find_element(By.XPATH,'/html/body/div[4]/div/div[2]/section/div/div/div/form/div/center/button')
        browser.save_screenshot(save_path[0])
        try:
            fs_button=browser.find_element(By.XPATH,'/html/body/div[4]/div/div[2]/section/div/div/div/form/div/center/button')
            fs_button.click()    
        except StaleElementReferenceException as e:
            fs_button=browser.find_element(By.XPATH,'/html/body/div[4]/div/div[2]/section/div/div/div/form/div/center/button')
            fs_button.click()
           

        
        browser.implicitly_wait(5)
        browser.save_screenshot(save_path[1])
        browser.close()
        return 1

    except Exception as e:
        browserLog.exception(f"Site:{site_data['name']}")
        browser.save_screenshot(save_path[2])
        return -1

def radiance_(subproject, browser, site_data, lead_data, path):
    
    try:
        browserLog.info(f"Site: {site_data['name']}, Project:{subproject}")
        save_path=path
        phone=PN.parse(lead_data['phone'])
        phoneno=phone.national_number
        browser.get(site_data["url"])
        search=browser.find_element(By.XPATH,'/html/body/div[1]/div[1]/div/div/div[2]/div[3]/form/div[2]/div/input[1]')        
        search.send_keys(site_data["email"])
        time.sleep(1)
        pwdd=browser.find_element(By.XPATH,'//*[@id="password"]')
        pwdd.send_keys(site_data["pass"])
        submit=browser.find_element(By.XPATH,'/html/body/div[1]/div[1]/div/div/div[2]/div[3]/form/input[2]')
        submit.send_keys(Keys.RETURN)

        time.sleep(3)
        browser.get(site_data["url2"])

        time.sleep(3)
        newlead=browser.find_element(By.XPATH,'/html/body/div[3]/div[2]/div/div[2]/div/div/c-related-source-data-table-lwc/div[1]/div/div/div/div/div[3]/button[1]')
        newlead.send_keys(Keys.RETURN)
        time.sleep(3)
        
        namelead=browser.find_element(By.XPATH,'/html/body/div[3]/div[2]/div/div[2]/div/div/c-related-source-data-table-lwc/c-create-new-lead/section/div/div/div/div[1]/div[1]/div/div/input')
        namelead.send_keys(lead_data['name'])
        time.sleep(1)

        projectlead=browser.find_element_by_xpath('/html/body/div[3]/div[2]/div/div[2]/div/div/c-related-source-data-table-lwc/c-create-new-lead/section/div/div/div/div[1]/div[2]/div/lightning-combobox/div[1]/lightning-base-combobox/div/div[1]/button')
        projectlead.click()
        projectlead.send_keys(subproject)        
        projectlead.send_keys(Keys.RETURN)
        emaillead=browser.find_element(By.XPATH,'/html/body/div[3]/div[2]/div/div[2]/div/div/c-related-source-data-table-lwc/c-create-new-lead/section/div/div/div/div[2]/div[1]/div/div/lightning-input/div/input')
        emaillead.send_keys(lead_data['email'])
        time.sleep(1)        

        contact=browser.find_element(By.XPATH,'/html/body/div[3]/div[2]/div/div[2]/div/div/c-related-source-data-table-lwc/c-create-new-lead/section/div/div/div/div[2]/div[2]/div[2]/div/lightning-input/div/input')
        contact.send_keys(phoneno)
        time.sleep(1)

        commentsbox=browser.find_element(By.XPATH,'/html/body/div[3]/div[2]/div/div[2]/div/div/c-related-source-data-table-lwc/c-create-new-lead/section/div/div/div/div[4]/div/div/div/div/lightning-textarea/div/textarea')
        commentsbox.send_keys("None")
        time.sleep(1)
        browser.save_screenshot(save_path[0])
        submitbutton = browser.find_element(By.XPATH,'/html/body/div[3]/div[2]/div/div[2]/div/div/c-related-source-data-table-lwc/c-create-new-lead/section/div/footer/button[2]')
        submitbutton.click()

        time.sleep(3)
        browser.save_screenshot(save_path[1])
        return 1
    
    except Exception as e:
        browserLog.exception(f"Site:{site_data['name']}")
        browser.save_screenshot(save_path[2])
        return -1

def shriram(subproject:str, browser:Firefox, site_data:dict, lead_data:dict, path:list):   
    try:
        browserLog.info(f"Site: {site_data['name']}, Project:{subproject}")
        save_path=path
        browser.get(site_data["url"])
        phone=PN.parse(lead_data['phone'])
        phoneno=phone.national_number
    
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
        partner1.send_keys(site_data["channel_partner"])
        partner1.send_keys(Keys.RETURN)
        coustmer_name = browser.find_element(By.XPATH, '//*[@id="input_9_2"]')
        coustmer_name.send_keys(lead_data['name'])
        coustmer_email = browser.find_element(By.XPATH, '//*[@id="input_9_3"]')
        coustmer_email.send_keys(lead_data['email'])
        code = Select(browser.find_element(By.XPATH, '//*[@id="input_9_56"]'))
        code.select_by_visible_text('India (+91)')
        coustmer_phone = browser.find_element(By.XPATH, '//*[@id="input_9_4"]')
        coustmer_phone.send_keys(phoneno)
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
        area.select_by_visible_text(subproject)
        comment = browser.find_element(By.XPATH, '//*[@id="input_9_12"]')
        comment.send_keys('Nil')
        email10 = browser.find_element(By.XPATH, '//*[@id="input_9_47"]')
        email10.send_keys(site_data["email"])
        phone10 = browser.find_element(By.XPATH, '//*[@id="input_9_48"]')
        phone10.send_keys(site_data["mobile"])
        browser.save_screenshot(save_path[0])
        
 
        
        submit = browser.find_element(
            By.XPATH, '//*[@id="gform_submit_button_9"]')
        submit.click()
        time.sleep(20)

        try:
            aa = WebDriverWait(browser, 5).until(
            EC.presence_of_element_located(
                (By.XPATH,"/html/body/div[3]/div/div/div[3]/button"))
                # (By.XPATH, "//*[@id='gform_9']/div[1]"))
            )
            aa.click()
            
            # end=browser.find_element(By.XPATH,"/html/body/div[3]/div/div/div[3]/button")
            # end.click()
        except Exception as e:
            pass
        
        time.sleep(1)
        browser.save_screenshot(save_path[1])
        
        return 1


    except Exception as e:
        browserLog.exception(f"Site:{site_data['name']}")
        browser.save_screenshot(save_path[2])
        return -1


#working
def tvs(subproject:str,browser:Firefox,site_data:dict, lead_data:dict, path:list):
    try:
        browserLog.info(f"Site: {site_data['name']}, Project:{subproject}")
        save_path=path
        first_name,last_name=getName(lead_data['name'])
        browser.get(site_data["url"])
        phone_no= PN.parse(lead_data['phone'])    
        #search=browser.find_element(By.XPATH,'/html/body/div[2]/div/div[2]/section/div[1]/div/div[2]/div/form/fieldset[1]/input')
        search=browser.find_element(By.XPATH,'//*[@id="user_login"]')        
        search.send_keys(site_data["email"])
        #time.sleep(3)
        
        #name  = browser.find_element(By.NAME, "Pname")
        #name.send_keys(name1)        
        
        time.sleep(1)
        pwdd=browser.find_element(By.XPATH,'//*[@id="user_password"]')
        pwdd.send_keys(site_data["pass"])
        
        #passo=browser.find_element(By.XPATH,'/html/body/div[1]/div[1]/div/div/div[2]/div[3]/form/input[1]')
        #passo.send_keys(all_sites.sites[site_name]["pass"])
        time.sleep(1)        
        submit=browser.find_element(By.XPATH,'/html/body/section/div/div/div[1]/div/form[2]/div[4]/input')
        submit.send_keys(Keys.RETURN)

        time.sleep(6)
        #open new tab
        #browser.find_element(By.TAG_NAME,'body').send_keys(Keys.COMMAND + 't')
        browser.get(site_data["url2"])

        time.sleep(3)
        addlead=browser.find_element(By.XPATH,'/html/body/div[1]/section/div/div/div[2]/div/a')
        addlead.send_keys(Keys.RETURN)
        time.sleep(3)
        
        firstnamelead=browser.find_element(By.XPATH,'//*[@id="lead_first_name"]')
        firstnamelead.send_keys(first_name)
        time.sleep(1)

        lastnamelead=browser.find_element(By.XPATH,'//*[@id="lead_last_name"]')
        lastnamelead.send_keys(last_name)
        time.sleep(1)

        emaillead=browser.find_element(By.XPATH,'//*[@id="lead_email"]')
        emaillead.send_keys(lead_data['email'])
        time.sleep(1)                

        #projectlead=browser.find_element(By.XPATH,'/html/body/div[3]/div[2]/div/div[2]/div/div/c-related-source-data-table-lwc/c-create-new-lead/section/div/div/div/div[1]/div[2]/div/div/lightning-combobox/div[1]/lightning-base-combobox/div/div[1]/button')
        #projectlead=Select(browser.find_element(By.ID,'combobox-button-618'))
        #projectlead.select_by_visible_text("Radiance Maraikayar Manor")        
        #time.sleep(5) 

        #projectlead2=browser.find_element_by_xpath('/html/body/div[3]/div[2]/div/div[2]/div/div/c-related-source-data-table-lwc/c-create-new-lead/section/div/div/div/div[1]/div[2]/div/div/lightning-combobox/div/lightning-base-combobox/div/div[1]/button/span/text()')
	#/html/body/div[3]/div[2]/div/div[2]/div/div/c-related-source-data-table-lwc/c-create-new-lead/section/div/div/div/div[1]/div[2]/div/div/lightning-combobox/div/lightning-base-combobox/div/div[1]/button
        #projectlead2=browser.find_element_by_data-value(sub_project_name)    
        #projectlead2.click()            
        #time.sleep(5)       

        #namelead=browser.find_element(By.XPATH,'/html/body/div[3]/div[2]/div/div[2]/div/div/c-related-source-data-table-lwc/c-create-new-lead/section/div/div/div/div[1]/div[1]/div/div/div/input')
        #namelead.send_keys(name1)
        #time.sleep(1)

        #namelead=browser.find_element(By.XPATH,'/html/body/div[3]/div[2]/div/div[2]/div/div/c-related-source-data-table-lwc/c-create-new-lead/section/div/div/div/div[1]/div[1]/div/div/div/input')
        #namelead.send_keys(name1)
        #time.sleep(1)

        ## COUNTRY        
        #country2 = browser.find_element(By.XPATH, '/html/body/div[3]/div[2]/div/div[2]/div/div/c-related-source-data-table-lwc/c-create-new-lead/section/div/div/div/div[2]/div[2]/div[1]/div/lightning-combobox/div/lightning-base-combobox/div/div[1]/button')
        #country2.click()
        #time.sleep(1)        
        #country2.send_keys(country_name)
        #time.sleep(1)        
        #country2.send_keys(Keys.RETURN)
        #time.sleep(1)

        contact=browser.find_element(By.XPATH,'//*[@id="lead_phone"]')
        time.sleep(1)        
        contact.click()        
        time.sleep(1)
        contact.send_keys(Keys.BACKSPACE)
        time.sleep(1)
        contact.send_keys(Keys.BACKSPACE)
        time.sleep(1)
        contact.send_keys(Keys.BACKSPACE)
        time.sleep(1)
        contact.send_keys(Keys.BACKSPACE)
        time.sleep(1)        
        contact.send_keys(lead_data['phone'])         
        
        #contact.send_keys(phone)
        time.sleep(1)

        projectlead=browser.find_element(By.XPATH,'/html/body/div[3]/form/div/div/div/div[2]/div/div[2]/div[4]/div/div/div/div[1]')
        #projectlead=browser.find_element_by_xpath('/html/body/div[3]/form/div/div/div/div[2]/div/div[2]/div[4]/div/div/div/div[1]/div')        
        #time.sleep(5)        
        projectlead.click()
        #projectlead.send_keys("E")                
        #time.sleep(2) 
        #projectlead.send_keys(Keys.DOWN)        
        #projectlead.send_keys(sub_project_name)        
        #time.sleep(1)
        
        #projectlead.send_keys("Hello")
        #Smart Homes @ Green Enclave
        projectlead=browser.find_element(By.ID,'lead_project_id-selectized')
        projectlead.send_keys(subproject)                
        #time.sleep(10)        
        #projectlead.send_keys(Keys.ENTER)
        projectlead.send_keys(Keys.RETURN)        
        time.sleep(1)

      
        browser.save_screenshot(save_path[0])
        submitbutton = browser.find_element(By.XPATH,'/html/body/div[3]/form/div/div/div/div[3]/input')
        submitbutton.click()
        #browser.execute_script("arguments[0].click();", button)
        browser.save_screenshot(save_path[1])
        time.sleep(10)

        # browser.save_screenshot(save_path)    
        # browser.quit()
        # upload_an_attachment(lead_id, save_path)
        
        return 1
        # lead = Lead(name=name1, props= sub_project_name, phone = phone, email = email1, status = req, created_at =  dt_string, attachments = save_path)
        # db.session.add(lead)
        # db.session.commit()
        # print('Successfully added' + str(lead.id) + ' ' + str(sub_project_name) + ' ' + str(lead.status))
    
    
    except Exception as e:
        browserLog.exception(f"Site:{site_data['name']}")
        browser.save_screenshot(save_path[2])
        return -1
        

def vr(subproject, browser, site_data, lead_data, path):

    try:
        browserLog.info(f"Site: {site_data['name']}, Project:{subproject}")
        save_path=path
        browser.get(site_data["url"])

        name  = browser.find_element(By.XPATH, '//*[@id="last_name"]')
        name.send_keys(lead_data['name'])
        time.sleep(3)
        

        contact=browser.find_element(By.XPATH,'//*[@id="phone"]')
        contact.send_keys(lead_data['phone'])

        email=browser.find_element(By.XPATH,'//*[@id="email"]')
        email.send_keys(lead_data['email'])

        cpname  = browser.find_element(By.XPATH, '//*[@id="00N0o00000NVnu3"]')
        cpname.send_keys(site_data["partner_name"])

        cpemail=browser.find_element(By.XPATH,'//*[@id="00N0o00000OSmDr"]')
        cpemail.send_keys(site_data["partner_email"])
        time.sleep(3)
        
        project=Select(browser.find_element(By.XPATH,'/html/body/div/form/div/div[12]/div/select'))
        project.select_by_visible_text(subproject)
        time.sleep(1)        
        browser.save_screenshot(save_path[0])

        add=browser.find_element(By.XPATH,'/html/body/div/form/div/div[13]/div/button')
        add.click()
        time.sleep(3)
        browser.save_screenshot(save_path[1])
                
        return 1
        
    
    except Exception as e:
        browserLog.exception(f"Site:{site_data['name']}")
        browser.save_screenshot(save_path[2])

        return -1        
