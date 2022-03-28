import email
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoAlertPresentException
from selenium.common.exceptions import NoSuchElementException
from pymongo import MongoClient
from app.functions.browser_automation import *
from app.util.utility import getTime, getsavePath, send_mail, upload_an_attachment
import time
import os
from datetime import datetime, timedelta
import app.functions.Config as Config


# async def browsertimer(v_browser):
#     time.sleep(100)
#     v_browser.quit()
MONGO_USER = "REDACTED"
MONGO_PASSWORD = "REDACTED"
DRIVER = "./geckodriver"
MONGO_DB = "REDACTED"
WEBDRIVER_LOG = "webdriver.log"
project_store = {
    "adityaram": adityaram,
    "alliance": alliance,
    "akshaya": akshaya,  
    "brigade": brigade,
    "casagrand": casagrand,
    "dlf" : "dlf",
    "doshi": doshi,
    "dra": dra,  
    "fomra": fomra,  
    "gsquare": gsquare,  
    "hiranandani": hiranandani,
    # "incor":incor,
    "krishnagrp": krishnagrp,
    "lifestyle": lifestyle,
    "lancor":lancor, 
    "pragnya": pragnya,  
    "radiance": radiance,
    "radiance_phase_2":radiance_,
    "shriram"    : shriram,
    "tvs": tvs,
    "vijayaraja" : vr 

}


class SiteAutomator:
    def __init__(self, phone, email, lead_data, site_data) -> None:
        self.phone = phone
        self.email = email
        self.lead_data = lead_data
        self.path = ""
        self.result = 0
        self.site_data = site_data
        # DB
        self.CONN = MongoClient(MONGO_DB)
        self.DB = self.CONN['lead_automation']

        self.LEAD = self.DB["leads"]
        self.SITE = ""
        

        self.driver = DRIVER

        firefox_service = Service(self.driver)
        opt = Options()
        opt.add_argument("--incognito")

        # opt.add_argument("--headless")
        self.browser = webdriver.Firefox(
            options=opt,
            service=firefox_service,
            service_log_path=WEBDRIVER_LOG
        )

    def projectCheck(self, project, sub_project_name, keyword_search):
        try:

            # print(self.SITE['name'])
            print("db working")

            self.sub_project_name = sub_project_name

            if keyword_search == True:
                # key_value=self.KEYWORD.find_one({},{sub_project_name:1})
                # if key_value:
                #     temp_data=dict(*key_value)
                #     self.sub_project_name=temp_data[sub_project_name]
                # else:
                self.sub_project_name = Config.project_sub[sub_project_name]

                #  db.Keyword.find({},{"Fomra Vayou":1})
                # self.sub_project_namse = self.DB["Keyword"].find({},{"_id":0,:sub_project_name:1})

            filterdate = datetime.now()-timedelta(30)
            self.projectexist = self.LEAD.find_one(
                {
                    "email": self.lead_data["email"],
                    # "email": self.lead_data["email"],
                    "project": {
                        "$elemMatch":
                        {
                            "subproject": self.sub_project_name}
                    },
                    "project.applied_time":
                    {
                        "$gte": filterdate
                    },
                    "project.status":
                    {
                        "$eq": 1
                    }
                },
                {"project.$": 1})

            if self.projectexist:
                self.result = 0
                print("lead already exist")

        except Exception as e:
            print("Error occured due to "+str(e))
            # return -1, -1
        # self.automated_flow()

    def automated_flow(self):
        try:
            # if self.result=="failed":return
            if not self.projectexist:
                self.path = "./storage/"+self.site_data["name"]
                if not os.path.exists(self.path):
                    os.mkdir(self.path)
                self.automate_path = getsavePath(
                    self.path, self.site_data['name'], self.sub_project_name, self.lead_data['name'])
                v_automator = project_store[self.site_data['name']]
                self.result = v_automator(
                    self.sub_project_name, self.browser, self.site_data, self.lead_data, self.automate_path)
        except Exception as e:
            self.result = 2

    def upload_data(self):

        try:

            # ZOHO attachment
            if self.result == 1 or self.result == -1:
                if self.result == 1:

                    upload_an_attachment(
                        self.lead_data["lead_id"], os.path.abspath(self.automate_path[0]))
                    upload_an_attachment(
                        self.lead_data["lead_id"], os.path.abspath(self.automate_path[1]))
                    print("uploaded file : ", os.path.abspath(
                        self.automate_path[0]))
                    print("uploaded file : ", self.automate_path[1])
                    print("success lead uploaded")
                if self.result == -1:
                    if os.path.exists(self.automate_path[0]):
                        upload_an_attachment(
                            self.lead_data["lead_id"], os.path.abspath(self.automate_path[0]))
                    upload_an_attachment(
                        self.lead_data["lead_id"], os.path.abspath(self.automate_path[2]))
                    print("uploaded file : ", self.path[0])
                    print("uploaded file : ", self.path[2])
                    print("failed  lead uploaded")
                print("lead_id :", self.lead_data["lead_id"])
                print("lead path : ", self.path)
                print("attachments uploaded")
            if self.result == 2 or self.result == -1:
                send_mail(self.lead_data['lead_id'], self.path,
                          self.sub_project_name, self.lead_data['name'])
        # DB
            lead_detail = {
                "projectname": self.site_data['name'],  # akshaya
                "subproject": self.sub_project_name,  # Tango
                "applied_time": datetime.now(),
                "status": self.result,
            }
            self.LEAD.update_one(
                {
                    "email": self.lead_data["email"],
                    "phone": self.lead_data["phone"]
                },
                {
                    "$set":
                    {
                        "modified_time": datetime.now()
                    },
                    "$push":
                    {
                        "project": lead_detail
                    }
                })

            print("lead uploaded")
        except Exception as e:
            print(e)

    def teardown(self):
        self.browser.quit()
