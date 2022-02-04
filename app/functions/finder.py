import importlib
from pymongo import MongoClient
from app.functions import akshaya
from importlib import import_module
import os
def function_finder(lead_data):
    try:
        CONN=MongoClient("mongodb://REDACTED_MONGO_URI")
        DB = CONN['lead_automation']
        LEADS=DB['leads']
        SITE=DB['Site']
        print(SITE)
        print("db working")
        
    except Exception as e:
        print("Error occured due to "+str(e))
    
    try:
       
        project_name=lead_data.get("project_enquired_for")
        print("working before using db")
        site=SITE.find_one({"key_words":{"$in":[project_name]}})
        # site=SITE.find_one({"key_words":{"$in":["Akshaya Tango"]}}) 
        # print("site name :",site," ",)
        dyn_mod=import_module("."+site['name'],"app.functions")
        storage="./storage/"
        #project_enquire_for
        dyn_mod.addlead(site['name'],sub_project_name=project_name,storage=storage,**lead_data)
        for interested_site in lead_data["interested_properties"]:
            site=SITE.find_one({"key_words":{"$in":[interested_site]}})
            dyn_mod=import_module("."+site['name'],"app.functions")
            dyn_mod.addlead(site['name'],sub_project_name=interested_site,storage=storage,**lead_data)


        return "success"
    except Exception as e:
        print("error occured in function_finder",str(e))
        print(os.getcwd())
        return "failed"