from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoAlertPresentException
from selenium.common.exceptions import NoSuchElementException
from pymongo import MongoClient
from app.functions.browser_automation import *
from app.util.utility import getTime,getsavePath
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
project_store = {
     "alliance"   : alliance,
     "akshaya"    : akshaya,     #1
     "brigade"    : brigade,     #2
     "fomra"      : fomra,     #3
     "adityaran"  : "adityaram", #4
     "casagrand"  : "casagrand", #5
     "dra"        : "dra",       #6
     "tvs"        : "tvs",       #7
     "shriram"    : "shriram",   #8
     "radiance"   : "radiance",  #9
     "lifestyle"  : "lifestyle", #10
     "hiranadgani": "hirandani", #11
     "pragnya"    : "pragnya",   #12
     "doshi"      : "doshi",     #13
     "krishnagrp" : "krishnagrp",#14
     "gsquare"    : "gsquare"    #15

       }

class SiteAutomator:
    def __init__ ( self , phone , email,lead_data) -> None:
        self.phone = phone 
        self.email = email
        self.lead_data = lead_data
        self.SITE = ""
        self.LEAD = ""
        # self.lead_data=lead_data
        self.driver = DRIVER
        
        firefox_service = Service(self.driver)
        opt = Options()
        opt.add_argument ( "--incognito" )
        # opt.add_argument("--headless")
        self.browser = webdriver.Firefox ( 
            options = opt ,
            service = firefox_service
            )
    

    def projectCheck(self,project,sub_project_name,keyword_search):
        try:
            self.sub_project_name = Config.project_sub[sub_project_name]
            CONN=MongoClient(MONGO_DB)
            self.DB = CONN['lead_automation']
            self.LEAD=self.DB['leads'] #collectioncursor
            self.SITE=self.DB['Site'].find_one({"name":project}) #dictnoi
            print(self.SITE['name'])
            print("db working")
            filterdate=datetime.now()-timedelta(30)
            self.projectexist=self.LEAD.find_one(
                { 
                "email": self.lead_data["email"],
                "project": { 
                    "$elemMatch":
                        {
                            "subproject": self.sub_project_name} 
                        },
                "project.applied_time":
                    {"$gte": filterdate}
                },
                { "project.$": 1 })
            
            if self.projectexist :
                self.result ="failed"
                print("lead already exist")

        except Exception as e:
            print("Error occured due to "+str(e))
            # return -1, -1
        # self.automated_flow()
    
    def automated_flow( self):
        try:
            # if self.result=="failed":return
            if not self.projectexist:
                self.path="./storage/"+self.SITE["name"]
                if not os.path.exists(self.path):
                    os.mkdir(self.path)
                v_automator = project_store[ self.SITE['name'] ]
                self.result = v_automator(self.sub_project_name, self.browser , self.SITE , self.lead_data,self.path)
        except Exception as e :
            self.result="failed"


    def is_element_present(self,how,what):
        try: self.browser.find_element( by=how, value=what )
        except NoAlertPresentException: return False
    
    
    def is_alert_present(self):
        try: self.browser.switch_to_alert()
        except NoAlertPresentException as e: return False
    
    def upload_data( self):
        
        lead_detail = { 
            "projectname": self.SITE[ 'name' ],#akshaya
            "subproject": self.sub_project_name ,#Tango
            "applied_time": datetime.now() ,
            "status": self.result,
            }
        self.LEAD.update_one(
            {
                "email": self.lead_data[ "email" ] ,
                "phone": self.lead_data[ "phone" ] 
            },
            {
                "$set": 
                {
                    "modified_time" : datetime.now() 
                },
                "$push":
                {
                    "project": lead_detail
                }
            })
        
        print("lead uploaded")
        
    def teardown(self):
        self.browser.quit()
        
