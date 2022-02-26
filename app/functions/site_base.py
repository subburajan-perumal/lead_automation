from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from pymongo import MongoClient
from app.functions.browser_automation import akshaya
from app.util.utility import getTime,getsavePath
import time
import os
from datetime import datetime, timedelta
import app.functions.Config as Config

# async def browsertimer(v_browser):
#     time.sleep(100)
#     v_browser.quit()
project_store = { "akshaya" : akshaya }
class common_site_validation:
    def __init__ ( self , phone , email,lead_data) -> None:
        self.phone = phone 
        self.email = email
        self.lead_data = lead_data
        self.SITE = ""
        self.LEAD = ""
        # self.lead_data=lead_data
        self.driver = "./geckodriver"
        firefox_service = Service(self.driver)
        opt = Options()
        opt.add_argument ( "--incognito" )
        # opt.add_argument("--headless")
        self.browser = webdriver.Firefox ( 
            options = opt ,
            service = firefox_service
            )

    def projectCheck(self,project,sub_project_name):
        try:
            self.sub_project_name = Config.project_sub[sub_project_name]
            CONN=MongoClient("mongodb://REDACTED_MONGO_URI")
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
        if not self.projectexist:
            v_automator = project_store[ self.SITE['name'] ]
            self.result = v_automator(self.sub_project_name, self.browser , self.SITE , self.lead_data)


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
                "phone": self.lead_data["phone"] 
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
        
