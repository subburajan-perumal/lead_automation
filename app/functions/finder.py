from datetime import datetime
from pymongo import MongoClient
from app.functions.site_base import SiteAutomator
import logging
import os
MONGO_DB="REDACTED"


def function_finder(lead_data):
    try:
    #     logging.basicConfig("")
    #     logger=logging.getLogger()
    #     logger.level
        CONN=MongoClient(MONGO_DB)
        DB = CONN['lead_automation']
        LEADS=DB['leads']
        SITE=DB['Site']
        print(SITE)
        print("db working")
        
    except Exception as e:
        print("Error occured due to "+str(e))
    
    try:
        user_detail=LEADS.find_one({"email":lead_data["email"],"phone":lead_data["phone"]})
        print(user_detail)
        fullname=lead_data['first_name']+lead_data['last_name']
        if not user_detail:
            lead_creation={"name":fullname,
                    "phone":lead_data["phone"],
                    "email":lead_data["email"], 
                    "created_at":datetime.now(),
                    "modified_time":datetime.now()
                    }
            LEADS.insert_one(lead_creation)
    
        project_name=lead_data.get("project_enquired_for")
        print("working before using db")

        
        site=SITE.find_one({"key_words":{"$in":[project_name]}})
        if site:
            browser_automation = SiteAutomator( lead_data[ "phone" ] , lead_data[ "email" ],lead_data)
            browser_automation.projectCheck( site ['name'], project_name)
            browser_automation.automated_flow()
            browser_automation.upload_data()
            browser_automation.teardown()
            

        
        # site=SITE.find_one({"key_words":{"$in":["Akshaya Tango"]}}) 
        # print("site name :",site," ",)

        # LEADS.insert_one()
        # if not site:
            # return "failed"
            # pass
        # else:
            # dyn_mod=import_module("."+site['name'],"app.functions")
        
        storage="./storage/"
    
        #project_enquire_for
        # dyn_mod.addlead(site['name'],sub_project_name=project_name,storage=storage,**lead_data)
        # if "interested_properties" in lead_data:

        #     for interested_site in lead_data["interested_properties"].split(";"):
        #         site=SITE.find_one({"key_words":{"$in":[interested_site]}})
        #         if not site:
        #             continue
        #         dyn_mod=import_module("."+site['name'],"app.functions")
        #         dyn_mod.addlead(site['name'],sub_project_name=interested_site,storage=storage,**lead_data)
        # # for place in lead_data["localities"]:
        #     # pass
        # #bylocalities

            #omr-akshaya tango
        return "success"
    except Exception as e:
        print("error occured in function_finder",str(e))
        # print(os.getcwd())
        return "failed"