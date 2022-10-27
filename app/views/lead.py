import logging
from flask import Blueprint, render_template, request,jsonify
from app.database import mongo
from bson import json_util
import json
from pymongo import MongoClient
from app.functions.error_site_base import SiteAutomator1


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
                        if key == 'applied_time':
                            lead_detail[key] = value['$date']                                                  
                    for key, value in project.items():
                        lead_detail[key] = value
                        if key == 'applied_time':
                            lead_detail[key] = value['$date']                   
                    leads_details.append(lead_detail)
            leads_details = json.loads(json_util.dumps(leads_details))
            print("lead_all posted")
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
                    for key,value in project.items():
                        if key == 'match_keywords':
                            lead_detail[key] = value
                lead_detail['project'] = arr
                    # for key, value in project.items():
                    #     lead_detail[key] = value
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
def error_retry():
    return render_template('/lead/error_retry.html')

@lead.post("/error_retry")
def getvalue():
    if request.method == "POST":
        logging.error("error_retry_working")
        projectname = request.form['projectname']
        phone_no = request.form['phone_no']
        lead_id = request.form['lead_id']
        logging.error(projectname)
        logging.error(phone_no)
        logging.error(lead_id)
        try:
            MONGO_DB = "REDACTED"
            CONN = MongoClient(MONGO_DB)
            DB = CONN['lead_automation']
            logging.error("data connected successfully")

            #site_data

            site_data = DB.Site.find_one({"project_list.project_name": projectname})
            logging.error(site_data)
            logging.error("site data fetched successfully")

            #lead_data

            lead_data  = DB.leads.find_one({'phone': phone_no})
            logging.error(lead_data)
            logging.error("lead data fetched successfully")

            site_name = site_data['name']
            logging.error("site_name" + site_name)
            site_projectname = projectname
            logging.error("projectname" + projectname)
            browserAutomation = SiteAutomator1(  
                                            phone = lead_data["phone"],
                                            email= lead_data["email"],
                                            lead_data= lead_data,
                                            match_keywords= [],
                                            site_data= site_data,
                                            sub_project_name = site_projectname,
                                            lead_id = lead_id
                                            )
            # browserAutomation.projectCheck(site_name, site_projectname)
            logging.error("browser_automation working")
            browserAutomation.automated_flow()
            logging.error("browser automation automated_flow")
            browserAutomation.upload_data()
            logging.error("browser automation upload_data")
            browserAutomation.teardown()
            logging.error("browser automation teardown")
        
        
        
        except Exception as e:
            logging.error("error in whole function")
            return jsonify({"Status": "Error", "Error": str(e)})


    return render_template("/lead/error_retry_output.html")