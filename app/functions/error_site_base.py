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
from flask import Blueprint, render_template, request,jsonify

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
    "arun_excello" : arun_excello,
    "urban_tree" : urban_tree,
    "xs_real" : xs_real
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


class SiteAutomator1:

    def __init__(self, phone, email, lead_data, match_keywords, site_data,sub_project_name,lead_id) -> None:
        logger.error("site_automator_data")
        logger.error(phone)
        logger.error(email)
        logger.error(lead_data)
        logger.error(match_keywords)
        logger.error(site_data)
        self.email = email
        self.phone = phone
        self.lead_data = lead_data
        self.lead_id = lead_id
        self.path = ""
        self.result = 0
        self.site_data = site_data
        self.CONN = MongoClient(os.getenv("MONGO_DB", MONGO_DB))
        self.DB = self.CONN['lead_automation']
        self.match_keywords = match_keywords

        self.LEAD = self.DB["leads"]
        self.SITE = ""
        self.field_flag = None
        self.projectexist = False
        self.sub_project_name = sub_project_name
        logger.error("subprojectname")
        logger.error(self.sub_project_name )

        self.driver = Config.WEB_DRIVER

        firefox_service = Service(self.driver)
        opt = Options()
        opt.add_argument("--headless")
        logger.error("firefox executed")

        # opt.add_argument("--headless")
        try:
            self.browser = webdriver.Firefox(
                options=opt,
                service=firefox_service,
                service_log_path=WEBDRIVER_LOG
            )
            logger.error("webdriver executed")
        
        except Exception as e:  
            logger.error("webdriver_error")
            logger.error(e)
            logging.error("Having problem in webdriver")  

    def projectCheck(self, project, sub_project_name):
        logger.error("project check")
        logger.error(project)
        logger.error(sub_project_name)
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

            # if self.projectexist:
            #     self.result = 0
            #     logger.info("lead already exist")
            #     # print("lead already exist")
            logger.error("project check completed")
            logger.error(self.projectexist)

        except Exception as e:
            logger.error("Error occured due to "+str(e))
            # return -1, -1
        # self.automated_flow()

    def automated_flow(self):
        logger.error("automated flow started")
        logger.error(self.result)
        try:
            # if self.result=="failed":return
            if not self.projectexist:
                self.path = "./storage/"+self.site_data["name"]
                logger.error("self path")
                logger.error(self.path)
                self.path_zoho = "./storage/"+ 'zoho'
                logger.error("self path zoho")
                logger.error(self.path_zoho)
                if not os.path.exists(self.path):
                    os.mkdir(self.path)
                if not os.path.exists(self.path_zoho):
                    os.mkdir(self.path_zoho)
                self.automate_path = getsavePath(
                    self.path, self.path_zoho, self.site_data['name'], self.sub_project_name, self.lead_data['name'],self.phone)
                logger.error(self.sub_project_name)
                logger.error(self.browser)
                logger.error(self.site_data)
                logger.error(self.lead_data)
                logger.error(self.automate_path)
                v_automator = project_store[self.site_data['name']]
                logger.error("v_automator")
                logger.error(v_automator)
                logger.error(type(v_automator))
                logger.error(self.site_data['name'])
                self.result = v_automator(
                   self.sub_project_name, self.browser, self.site_data, self.lead_data, self.automate_path)
                logger.error("automated flow working properly")
                logger.error(self.result)
        except Exception as e:
            self.result = 2
            logger.exception("automte flow error: {}".format(e))

        finally:
            self.upload_data()

    def upload_data(self):
        import shutil
        logger.error("upload data started")
        try:
            # ZOHO attachment
            if self.result == 1 or self.result == -1:
                try:
                    shutil.copy(self.automate_path[0], self.automate_path[3])
                    shutil.copy(self.automate_path[1], self.automate_path[4])
                    upload_an_attachment(
                        self.lead_id, os.path.abspath(self.automate_path[3]))
                    upload_an_attachment(
                        self.lead_id, os.path.abspath(self.automate_path[4]))
                    # print("upload lead working")
                    logger.info(f"upload file{ self.automate_path[3] }")
                    # print("uploaded file : ", os.path.abspath(self.automate_path[0]))
                    logger.info(f"upload file{ self.automate_path[4] }")
                    # print("uploaded file : ", self.automate_path[1])
                    logger.error("try statement 1 success")
                
                except:
                    upload_an_attachment(
                        self.lead_id, os.path.abspath(self.automate_path[0]))
                    upload_an_attachment(
                        self.lead_id, os.path.abspath(self.automate_path[1]))    
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
                            self.lead_id, os.path.abspath(self.automate_path[5]))
                        logger.info(f"upload file{ self.automate_path[5] }")
                        logger.error("try statement 2 success")

                    except:
                        # if os.path.exists(self.automate_path[0]):
                        # upload_an_attachment(
                        upload_an_attachment(
                            self.lead_id, os.path.abspath(self.automate_path[2]))
                        logger.info(f"upload file{ self.automate_path[2] }")

                logger.error('upload_data worked successfully')

                # print("uploaded file : ", self.path[0])

                # print("uploaded file : ", self.path[2])
                # print("failed  lead uploaded")
                logger.info(f"lead_id :{self.lead_id}")
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
                "match_keywords": list(self.match_keywords),
                "lead_id": self.lead_id
            }
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