from pymongo import MongoClient
from app.util.utility import getTime,getsavePath
import time
import os
from datetime import datetime, timedelta
import app.functions.Config as Config

#CHECK DATA
def projectCheck(project,sub_project_name,**lead_data):
    #database
    # print("sub_project_name")
     #Replace Keyword with Project Name
    try:
        sub_project_name = Config.project_sub[sub_project_name]
        CONN=MongoClient("mongodb://REDACTED_MONGO_URI")
        DB = CONN['lead_automation']
        LEADS=DB['leads']
        SITE=DB['Site'].find_one({"name":project})
        print(SITE['name'])
        print("db working")
        filterdate=datetime.now()-timedelta(30)
        projectexist=LEADS.find_one(
            { 
            "email": lead_data["email"],
            "project": { 
                "$elemMatch":
                    {
                        "subproject": sub_project_name} 
                    },
            "project.applied_time":
                {"$gte": filterdate}
            },
            { "project.$": 1 })
        if projectexist :
            print("lead already exist")
            return -1, -1
    except Exception as e:
        print("Error occured due to "+str(e))
        return -1, -1
    return SITE, LEADS

