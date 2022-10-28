from datetime import datetime
import json
import logging
from celery.result import AsyncResult
from flask import Blueprint, Response, jsonify, redirect, render_template, request
from config import Config
from app.util.utility import bulk_mapping
from app.util.request_handler import find_format
import time
from app.tasks import lead, bulk_lead


# from .. import tasks
logging.basicConfig(
    # filename= Config.LOG_PATH+"lead_automation.log",
    level=logging.INFO,
    # format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s',
    encoding='utf-8'
    )


# blueprint for the app route
home = Blueprint("home", __name__)

secret_key="REDACTED_FLASK_SECRET"

@home.get("/tasks/<task_id>")
def get_status(task_id):
    logging.info(msg=request.get_data())
    task_result = AsyncResult(task_id, backend=Config.CELERY_RESULT_BACKEND)
    result = {
        "task_id": task_id,
        # "task_status": task_result.status,
        # "task_result": task_result.result
    }
    return jsonify(result), 200


@home.route("/test")
def test_page():
    return "site working"


@home.post("/")
def homepage_post():
    try:
        logging.info(msg="request received")
        logging.info(msg=request.headers)
        logging.info(msg=request.get_data())
        start_time = time.time()
        data = {}
        # out = "{}"
        print(request)
        print(request.get_data())

        # print(request.get_json())
        data = find_format(request)
        if data == {}:
            return Response("invalid request", 200)
        if type(data) is list:
            print(data)
        elif type(data) is dict:
            data['source'] = "zoho"
            print(data)
            result = lead.apply_async(kwargs=data, queue="lead")
            print("task executed succesfully")
            # print(result.task_id)
            # out={"task id" : result.task_id}
        else:
            print(data)

        end_time = time.time()
        print(f"Response time {end_time-start_time}")
        return Response("received", 200)

    except Exception as e:
        print(str(e))
        logging.info("invalid request received")
        return Response("something went wrong\n", status=400)


def retry_mapping(lead):
    data = {
        'interested_properties': lead['subproject'],
        'email': lead['email'],
        'name': lead['name'],
        'phone': lead['phone']
    }
    return data


@home.post("/retry_leads")
def webhook_retry():
    try:
        logging.info(msg="retry_leads request received")
        logging.info(msg=request.headers)
        start_time = time.time()
        data = {}
        print(request)
        print(request.get_data())
        data = find_format(request)
        if data == {}:
            return Response("invalid request", 200)
        if type(data) is list:
            print(data)
        elif type(data) is dict:
            data['source'] = "retry"
            result = lead.apply_async(kwargs=retry_mapping(data), queue="lead")
            print("task executed succesfully")
        else:
            print(data)
        end_time = time.time()
        print(f"Response time {end_time-start_time}")
        return Response("received", 200)

    except Exception as e:
        print(str(e))
        logging.info("invalid request received")
        return Response("something went wrong\n", status=400)


# UPLOAD

@home.route('/bulk_leads_list')
async def bulk_leads():
    from app.database import mongo
    from bson import json_util
    try:
        db=mongo.db
        db = db["bulk_leads"]
        x=[]
        cur = db.find({'source': 'bulk_upload'}).sort("_id",-1).limit(50)
        result=json.loads(json_util.dumps(cur))
        leads_details = []
        for lead in result:
            lead['phone'] = lead['phone'][1:]
            lead_detail = dict()
            for key, value in lead.items():
                lead_detail[key] = value
                if key == "created_time":
                    lead_detail[key] = value['$date']
                    lead_detail[key] = str(lead_detail[key]).split(".")[0]
                    lead_detail[key] = datetime.strptime(str(lead_detail[key]), "%Y-%m-%dT%H:%M:%S")    
                    lead_detail[key] = lead_detail[key].strftime("%d/%m/%Y") + " " + lead_detail[key].strftime("%H:%M:%S") 
            leads_details.append(lead_detail)                
        leads_details = json.loads(json_util.dumps(leads_details))

        return render_template('/bulk/list.html', x=leads_details)
    except Exception as e:
        return jsonify({"Status": "Error", "Error": str(e)})

       # for i in result:
        #     i['phone'] = i['phone'][1:]
        #     x.append(i)
        #     for key,value in i.items():
        #         if key == "created_time":
        #             i[key] = value["$date"]
        #             i[key] = str(i[key]).split(".")[0]
        #             i[key] = datetime.strptime(str(i[key]), "%Y-%m-%dT%H:%M:%S")    
        #             i[key] = i[key].strftime("%d/%m/%Y") + " " + i[key].strftime("%H:%M:%S") 
        #         x.append(i) 



# UPLOAD BULK CSV

@home.route("/bulk_upload", methods=["GET","POST"])
async def uploader_file():
    from app.database import mongo
    import pandas as pd

    if request.method == "GET":
        return render_template("/bulk/upload.html")
    if request.method == "POST":
        logging.info(msg="Bulk upload request received")
        print('Bulk upload request received')
        try:
            f = request.files['file']
            db=mongo.db
            df = pd.read_csv(f)
            data = df.to_dict(orient="records")
            for val in data:
                try:
                    lead_data = bulk_mapping(val)
                    val = bulk_mapping(val)
                    val['created_time'] = datetime.now()
                    lead_data['source'] = 'bulk_upload'
                    val['source'] = 'bulk_upload'
                    db.bulk_leads.update_one(
                        {
                            'lead_phone': val['phone']
                        },
                        {
                            '$set': val
                        },
                        upsert = True
                    )
                    # db.bulk_leads.insert_one(val)
                    logging.info(msg='Lead raw')
                    logging.info(msg=val)
                    logging.info(msg='Lead parsed')
                    logging.info(msg=lead_data)
                    result = bulk_lead.apply_async(kwargs=lead_data, queue="bulk")
                    # result = lead.apply_async(kwargs=lead_data, queue="lead")
                    logging.info(msg='Added to bulk tasks')
                    logging.info(msg=result)
                    print(result)
                except:
                    pass
        except:
            pass
        return redirect('http://automation.example.com/bulk_leads_list')
