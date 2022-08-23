import logging
from flask import Blueprint, render_template
from app.database import mongo
from bson import json_util
import json

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
                    for key, value in project.items():
                        lead_detail[key] = value
                    leads_details.append(lead_detail)
            leads_details = json.loads(json_util.dumps(leads_details))
        except:
            leads_details = lead_all
        return render_template("/lead/new_leads.html", data=leads_details)
    except Exception as e:
        return(str(e))


@lead.get("/today")
def lead_today():
    try:
        db=mongo.db
        lead_all = db.leads.find({"project":{"$exists":"true"}},{"_id":0}).sort("_id",-1).limit(50)
        result=json.loads(json_util.dumps(lead_all))
        return render_template("/lead/view.html",data=result)
    except Exception as e:
        return(str(e))
