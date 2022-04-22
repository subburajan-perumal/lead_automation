import logging
from celery.result import AsyncResult
from flask import Blueprint, Response, jsonify, render_template, request
from config import Config
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

@lead.get("/today")
def lead_today():
    
    try:
        db=mongo.db;
        ls=[]
        lead_all = db.leads.find({"project":{"$exists":"true"}},{"_id":0}).sort("_id",-1).limit(50)
        # print(lead_all)
        # for i in lead_all:
        #     ls.append(i)
        result=json.loads(json_util.dumps(lead_all))
        # result=jsonify([i for i in lead_all])
        return render_template("/lead/view.html",data=result)

    except Exception as e:
        return(str(e))
    # render_template("message.html",message=lead_all)
