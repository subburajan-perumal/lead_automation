from selenium.webdriver import Firefox
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support import expected_conditions as EC
from phonenumbers import geocoder as GC
import phonenumbers as PN
import time
import logging
logging.basicConfig(filename="execution.log",
    level=logging.INFO,
    format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s'
    )
browserLog=logging.getLogger("browser_log.log")

# browserLog.setLevel=logging.INFO


driver="./geckodriver.exe"
firefox_service = Service(driver)
opt = Options()
opt.add_argument ( "--incognito" )
browser = webdriver.Firefox ( 
                            options = opt ,
                            service = firefox_service,
                            # service_log_path=WEBDRIVER_LOG
                            )

lead_data={
    "lead_id": "920786000234230275",
     "name": "Manikandan",
      "first_name": "",
    "last_name": "Manikandan", 
    "email": "redacted@example.com", 
    "phone": "9000000000",
     "project_enquired_for": "",
      "interested_properties": "SPR Market of India", 
      "interested_localities": "Perambur",
       "initial_enquiry_particulars_automation": ""
    }

site_data={"_id":{"$oid":"623c25874dca8f32e9244179"},"name":"alliance","url":"https://partners.allianceprojects.in/login","email":"redacted@example.com","pass":"REDACTED","status":1,"project_list":[{"project_name":"Alliance Galleria Residences","keywords":["Alliance Galleria","None (default)","LightHouse","Light House","Infinys","Tango","Shriram Park 63","alliancegalleria","Amethyst","Winchester","Radiance Pride","Radiance The Pride","Tuxedo","Elevate 21","Mandarin","AllianceTest"],"location":[]},{"project_name":"Villabelvedere/Eternity","keywords":["Urbanrise Eternity","Poonamal","Porur"],"location":["Porur"]},{"project_name":"Jubilee Residences","keywords":["Guduvanche","Lumina","Perungalathur"],"location":["Perungalathur"]},{"project_name":"Villabelvedere","keywords":[],"location":[]},{"project_name":"Humming Gardens","keywords":["Gardenia","Adityaram","Alliance Galleria","Alliance Humming Gardens","Hamlet","Perungalathur"],"location":["Perungalathur"]},{"project_name":"OMR Cluster","keywords":["Zenith","Courtyards","Risington","Amethyst","None (default)","Gold Standard","Sholinganallur","Siruseri","Egattur","Kelambakkam","Padur","OMR"],"location":["Sholinganallur","Siruseri","Egattur","Kelambakkam","Padur","OMR"]},{"project_name":"Orchidspringss","keywords":[],"location":[]},{"project_name":"Codename Newporur","keywords":[],"location":[]}]}

#issue in handling subproject
def alliance(subproject:str, browser:Firefox, site_data:dict, lead_data:dict, automate_path:list):
    try:
        # subproject_2=""
        # Villabelvedere/Eternity
        # if subproject=="Villabelvedere":
        #     subproject="Villabelvedere/Eternity"
        #     subproject_2="Villabelvedere"
        
        # if subproject=="Urbanrise Eternity":
        #     subproject="Villabelvedere/Eternity"
        #     subproject_2="Urbanrise Eternity"
        
        # # OMR Cluster - JS/CNCB,CNGS
        # if subproject=="Codename Chennai's Best":
        #     subproject="OMR Cluster - JS/CNCB,CNGS"
        #     subproject_2="Codename Chennai's Best"

        # if subproject=="Codename Gold Standard":
        #     subproject="OMR Cluster - JS/CNCB,CNGS"
        #     subproject_2="Codename Gold Standard"
        
        # if subproject=="Jasmine springs":
        #     subproject="OMR Cluster - JS/CNCB,CNGS"
        #     subproject_2="Jasmine springs"


        save_path = automate_path
        fullname=str(lead_data['name'])
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
        contact.send_keys(lead_data['phone'])
        email=browser.find_element(By.NAME,'email')
        email.send_keys(lead_data['email'])
        project=Select(browser.find_element(By.ID,'select_project'))
        project.select_by_visible_text(subproject)
        # if subproject_2 != "" :
            # projectsub=Select(browser.find_element(By.ID,'sub_project_select'))
            # projectsub.select_by_visible_text(subproject_2)


        # browser.save_screenshot(save_path[0])    

        add=browser.find_element(By.ID,'lead_submit_btn').click()
        aa = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.XPATH,"//*[@id='kt_table_1']/tbody/tr[1]/td[7]"))
        )
        # browser.save_screenshot(save_path[0])
        aa.click()
        
        time.sleep(5) ## FOR CHANGING WAIT TIME
        # browser.save_screenshot(save_path[1])
        browser.close()
        return 1
    except Exception as e:
        print(str(e))
        # browser.save_screenshot(save_path[2])
        return -1


subproject="Revolution One - Padur"
# subproject="Villabelvedere/Eternity"
path="./geckodriver.exe"
alliance(subproject, browser, site_data, lead_data, path)

# # subproject = 'Crown'
# browser = webdriver.Firefox(executable_path='./geckodriver.exe')
# result=alliance("Jasmine springs", browser, site_data, lead_data, ".")
# print(result)