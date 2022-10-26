from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from pymongo import MongoClient
from app.functions.browser_automation import *
from app.util.utility import getTime, getsavePath, send_mail, upload_an_attachment
import os
from datetime import datetime, timedelta
from celery.utils.log import get_task_logger
from config import Config

logger = get_task_logger(__name__)

# async def browsertimer(v_browser):
#     time.sleep(100)
#     v_browser.quit()
MONGO_USER = "REDACTED"
MONGO_PASSWORD = "REDACTED"
print(os.curdir)
# DRIVER ="/home/subburaj/LEAD_AUTOMATION/lead_automation/geckodriver"

MONGO_DB = "REDACTED"
WEBDRIVER_LOG = "webdriver.log"

project_store = {
    "adityaram": adityaram,
    "alliance": alliance,
    "akshaya": akshaya,
    "brigade": brigade,
    "casagrand": casagrand,
    "dlf": dlf,
    "doshi": doshi,
    "dra": dra,
    "fomra": fomra,
    "gsquare": gsquare,
    "hiranandani": hiranandani,
    # "incor":incor,
    "krishnagrp": krishnagrp,
    "lifestyle": lifestyle,
    "lancor": lancor,
    "pragnya": pragnya,
    "radiance": radiance,
    "radiance_phase_2": radiance_,
    "sidharth": sidharth,
    "shriram": shriram,
    "tvs": tvs,
    "vijayaraja": vr,
    "xs": xs,
}
required_store = {
    "adityaram": {"function": adityaram, "required_field": ["phone", "email"]},
    "alliance": {"function": alliance, "required_field": ["phone"]},
    "akshaya": {"function": akshaya, "required_field": ["phone"]},
    "brigade": {"function": brigade, "required_field": ["email", "phone"]},
    "casagrand": {"function": casagrand, "required_field": ["phone"]},

    # country cod also need for dlf
    "dlf": {"function": dlf, "required_field": ["phone"]},
    "doshi": {"function": doshi, "required_field": ["phone"]},
    "dra": {"function": dra, "required_field": ["phone"]},
    "fomra": {"function": fomra, "required_field": ["email", "phone"]},
    "gsquare": {"function": gsquare, "required_field": ["email", "phone"]},

    # countrycode not required
    "hiranandani": {"function": hiranandani, "required_field": ["email", "phone"]},
    "krishnagrp": {"function": krishnagrp, "required_field": ["email"]}
}


class SiteAutomator:

    def __init__(self, phone, email, lead_data, match_keywords, site_data) -> None:
        self.email = email
        self.lead_data = lead_data
        self.path = ""
        self.result = 0
        self.site_data = site_data
        self.CONN = MongoClient(os.getenv("MONGO_DB", MONGO_DB))
        self.DB = self.CONN['lead_automation']
        self.match_keywords = match_keywords

        self.LEAD = self.DB["leads"]
        self.SITE = ""
        self.field_flag = None

        self.driver = Config.WEB_DRIVER

        firefox_service = Service(self.driver)
        opt = Options()
        opt.add_argument("--incognito")

        # opt.add_argument("--headless")
        self.browser = webdriver.Firefox(
            options=opt,
            service=firefox_service,
            service_log_path=WEBDRIVER_LOG
        )

    def projectCheck(self, project, sub_project_name):
        try:

            logger.info("checking for existing project in db")
            self.sub_project_name = sub_project_name

            try:
                days = int(self.site_data['days'])
            except:
                days = 30

            filterdate = datetime.now()-timedelta(days)
            self.projectexist = self.LEAD.find_one(
                {
                    "email": self.lead_data["email"],
                    "project": {
                        "$elemMatch":
                        {
                            "subproject": self.sub_project_name
                        }
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
                logger.info("lead already exist")
                # print("lead already exist")

        except Exception as e:
            print("Error occured due to "+str(e))
            # return -1, -1
        # self.automated_flow()

    def automated_flow(self):
        try:
            # if self.result=="failed":return
            if not self.projectexist:
                self.path = "./storage/"+self.site_data["name"]
                self.path_zoho = "./storage/"+ 'zoho'
                if not os.path.exists(self.path):
                    os.mkdir(self.path)
                if not os.path.exists(self.path_zoho):
                    os.mkdir(self.path_zoho)
                self.automate_path = getsavePath(
                    self.path, self.path_zoho, self.site_data['name'], self.sub_project_name, self.lead_data['name'])
                v_automator = project_store[self.site_data['name']]
                self.result = v_automator(
                   self.sub_project_name, self.browser, self.site_data, self.lead_data, self.automate_path)
        except Exception as e:
            self.result = 2
            logger.exception("automte flow error: {}".format(e))

        finally:
            self.upload_data()

    def upload_data(self):
        import shutil

        try:
            # ZOHO attachment
            if self.result == 1 or self.result == -1:
                try:
                    shutil.copy(self.automate_path[0], self.automate_path[3])
                    shutil.copy(self.automate_path[1], self.automate_path[4])
                    upload_an_attachment(
                        self.lead_data["lead_id"], os.path.abspath(self.automate_path[3]))
                    upload_an_attachment(
                        self.lead_data["lead_id"], os.path.abspath(self.automate_path[4]))
                    # print("upload lead working")
                    logger.info(f"upload file{ self.automate_path[3] }")
                    # print("uploaded file : ", os.path.abspath(self.automate_path[0]))
                    logger.info(f"upload file{ self.automate_path[4] }")
                    # print("uploaded file : ", self.automate_path[1])
                
                except:
                    upload_an_attachment(
                        self.lead_data["lead_id"], os.path.abspath(self.automate_path[0]))
                    upload_an_attachment(
                        self.lead_data["lead_id"], os.path.abspath(self.automate_path[1]))    
                    # print("upload lead working")
                    logger.info(f"upload file{ self.automate_path[0] }")
                    # print("uploaded file : ", os.path.abspath(self.automate_path[0]))
                    logger.info(f"upload file{ self.automate_path[1] }")
                    # print("uploaded file : ", self.automate_path[1])

                # print("upload lead working")
                # logger.info(f"upload file{ self.automate_path[3] }")
                # print("uploaded file : ", os.path.abspath(self.automate_path[0]))
                # logger.info(f"upload file{ self.automate_path[4] }")
                # print("uploaded file : ", self.automate_path[1])
                # print("success lead uploaded")
                if self.result == 2 or self.result == -1:
                    try:
                        shutil.copy(self.automate_path[2], self.automate_path[5])
                        # if os.path.exists(self.automate_path[0]):
                        # upload_an_attachment(
                        upload_an_attachment(
                            self.lead_data["lead_id"], os.path.abspath(self.automate_path[5]))
                        logger.info(f"upload file{ self.automate_path[5] }")

                    except:
                        # if os.path.exists(self.automate_path[0]):
                        # upload_an_attachment(
                        upload_an_attachment(
                            self.lead_data["lead_id"], os.path.abspath(self.automate_path[2]))
                        logger.info(f"upload file{ self.automate_path[2] }")


                # print("uploaded file : ", self.path[0])

                # print("uploaded file : ", self.path[2])
                # print("failed  lead uploaded")
                logger.info(f"lead_id :{self.lead_data['lead_id']}")
                print(f"lead path :  {self.path}")
                # print("lead_id :", self.lead_data["lead_id"])
                logger.info("attachments uploaded")
                # print("attachments uploaded")
            	#if self.result == 2 or self.result == -1:
                #send_mail(self.lead_data['lead_id'], self.path,
                #          self.sub_project_name, self.lead_data['name'])
                #logger.info("mail sent")
            # DB
            lead_detail = {
                "projectname": self.site_data['name'],  # akshaya
                "subproject": self.sub_project_name,  # Tango
                "applied_time": getTime(),
                "status": self.result,
                "match_keywords": list(self.match_keywords)
            }
            print("Inserting lead detail")
            print(lead_detail)
            dbresult = self.LEAD.update_one(
                {
                    "email": self.lead_data["email"],
                    "phone": self.lead_data["phone"]
                },
                {
                    "$set":
                    {
                        "modified_time": getTime()
                    },
                    "$push":
                    {
                        "project": lead_detail
                    }
                })
            logger.info("lead uploaded")
            # print("lead uploaded")
            return dbresult.upserted_id
        except Exception:
            logger.exception("error occured in automation")
            dbresult = -1
            return dbresult

    def teardown(self):
        self.browser.quit()
        logger.info("browser quit")