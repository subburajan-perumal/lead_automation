import logging
from flask import Blueprint, render_template, request,jsonify
from app.database import mongo
from bson import json_util
import json
from pymongo import MongoClient
from app.functions.site_base import SiteAutomator


# from .. import tasks
logging.basicConfig(
    # filename= Config.LOG_PATH+"lead_automation.log",
    level=logging.INFO,
    format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s',
    encoding='utf-8'
    )


# blueprint for the app route
lead = Blueprint("lead", __name__,url_prefix="/lead")


@lead.get("/all")
def leads_all():
    try:
        db=mongo.db
        lead_all = db.leads.find({"project":{"$exists":"true"}},{"_id":0}).sort("_id",-1).limit(100)
        lead_all = json.loads(json_util.dumps(lead_all))
        leads_details = []
        try:
            for lead in lead_all:
                for project in lead['project']:
                    lead_detail = dict()
                    for key, value in lead.items():
                        if key != 'project':
                            lead_detail[key] = value
                        if key == 'created_at':
                            lead_detail[key] = value['$date']
                        if key == 'modified_time':
                            lead_detail[key] = value['$date']                            
                    for key, value in project.items():
                        lead_detail[key] = value
                    leads_details.append(lead_detail)
            leads_details = json.loads(json_util.dumps(leads_details))
        except:
            leads_details = lead_all
        return render_template("/lead/leads.html", data=leads_details)
    except Exception as e:
        return(str(e))


@lead.get("/today")
def lead_today():
    try:
        db=mongo.db
        lead_all = db.leads.find({"project":{"$exists":"true"}},{"_id":0}).sort("_id",-1).limit(50)
        lead_all = json.loads(json_util.dumps(lead_all))
        leads_details = []
        try:
            for lead in lead_all:
                arr = []
                for project in lead['project']:
                    lead_detail = dict()
                    for key, value in lead.items():
                        if key != 'project':
                            lead_detail[key] = value
                        if key == 'created_at':
                            lead_detail[key] = value['$date']
                        if key == 'modified_time':  
                            lead_detail[key] = value['$date']                            
                    for key, value in project.items():
                        if key == 'projectname':
                            arr.append(value)
                        if key == 'subproject':
                            arr.append(value)
                lead_detail['project'] = arr
                leads_details.append(lead_detail)
            leads_details = json.loads(json_util.dumps(leads_details))
        except:
            pass
        return render_template("/lead/view.html", data=leads_details)
    except Exception as e:
        return(str(e))

    except Exception as e:
        return(str(e))


@lead.get("/error_retry")
def index():
    return render_template('/lead/error_retry.html')

@lead.post("/error_retry")
def getvalue():
    if request.method == "POST":
        projectname = request.form['projectname']
        phone_no = request.form['phone_no']
        print(projectname, phone_no)
        try:
            MONGO_DB = "REDACTED"
            CONN = MongoClient(MONGO_DB)
            DB = CONN['lead_automation']

            #site_data

            site_data = DB.Site.find_one({"project_list.project_name": projectname})
            print(site_data)
            print("site data fetched successfully")

            #lead_data

            lead_data  = DB.leads.find_one({'phone': phone_no})
            print(lead_data)
            print("lead data fetched successfully")

            site_name = site_data['name']
            site_projectname = projectname
            browserAutomation = SiteAutomator(  
                                            phone = lead_data["phone"],
                                            email= lead_data["email"],
                                            lead_data= lead_data,
                                            match_keywords= None,
                                            site_data= site_data
                                            )
            browserAutomation.projectCheck(site_name, site_projectname)
            print("browser automation worked for error retry successfully")
            browserAutomation.automated_flow()
            browserAutomation.upload_data()
            browserAutomation.teardown()
        
        
        
        except Exception as e:
            return jsonify({"Status": "Error", "Error": str(e)})


    return 'data collected'