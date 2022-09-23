from datetime import datetime
import logging
from urllib import response
from celery.result import AsyncResult
from flask import Blueprint, Response, jsonify, redirect, render_template, request
from config import Config
from app.util.utility import bulk_mapping
from app.util.request_handler import find_format
import time
from app.tasks import lead

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


@home.get("/99acres")
def get_99acres():
    # logging.info(msg=request.get_data())
    # return {"message":"99 acres endpoint working"}
    
    from app.util.utility import insert_record_to_zoho

    try:
        logging.info(msg="99acres request received")
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
            data['source'] = "99acres"
            print(data)
            result = lead.apply_async(kwargs=data, queue="lead")
            _ = insert_record_to_zoho(data)
            print("task executed succesfully")
            # print(result.task_id)
            # out={"task id" : result.task_id}
        else:
            print(data)

        # insert_record_to_zoho(data)

        end_time = time.time()
        print(f"Response time {end_time-start_time}")
        return Response("received", 200)

    except Exception as e:
        print(str(e))
        logging.info("invalid request received")
        return Response("something went wrong\n", status=400)



@home.post("/99acres")
def webhook_99acres():
    from app.util.utility import insert_record_to_zoho

    try:
        logging.info(msg="99acres request received")
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
            data['source'] = "99acres"
            print(data)
            result = lead.apply_async(kwargs=data, queue="lead")
            _ = insert_record_to_zoho(data)
            print("task executed succesfully")
            # print(result.task_id)
            # out={"task id" : result.task_id}
        else:
            print(data)

        # insert_record_to_zoho(data)

        end_time = time.time()
        print(f"Response time {end_time-start_time}")
        return Response("received", 200)

    except Exception as e:
        print(str(e))
        logging.info("invalid request received")
        return Response("something went wrong\n", status=400)


@home.get("/magicbricks")
def get_magicbricks():
    # logging.info(msg=request.get_data())
    # return {"message":"magicbricks endpoint working"}
    from app.util.utility import insert_record_to_zoho

    try:
        logging.info(msg="magicbricks request received")
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
            data['source'] = "magicbricks"
            print(data)
            result = lead.apply_async(kwargs=data, queue="lead")
            _ = insert_record_to_zoho(data)
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



@home.post("/magicbricks")
def webhook_magicbricks():
    from app.util.utility import insert_record_to_zoho

    try:
        logging.info(msg="magicbricks request received")
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
            data['source'] = "magicbricks"
            print(data)
            result = lead.apply_async(kwargs=data, queue="lead")
            _ = insert_record_to_zoho(data)
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


        
@home.get("/housing")
def get_housing():
    # logging.info(msg=request.get_data())
    # return {"message":"housing endpoint working"}
    
    from app.util.utility import insert_record_to_zoho

    try:
        logging.info(msg="housing request received")
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
            data['source'] = "housing"
            print(data)
            result = lead.apply_async(kwargs=data, queue="lead")
            _ = insert_record_to_zoho(data)
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



@home.post("/housing")
def webhook_housing():
    from app.util.utility import insert_record_to_zoho

    try:
        logging.info(msg="housing request received")
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
            data['source'] = "housing"
            print(data)
            result = lead.apply_async(kwargs=data, queue="lead")
            _ = insert_record_to_zoho(data)
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
    try:
        db=mongo.db
        db = db["bulk_leads"]
        x=[]
        cur = db.find({'source': 'bulk_upload'})
        for i in cur:
            x.append(i)
        return render_template('/bulk/list.html', x=x)
    except Exception as e:
        return jsonify({"Status": "Error", "Error": str(e)})


# UPLOAD BULK CSV

@home.route("/bulk_upload", methods=["GET","POST"])
async def uploader_file():
    from app.database import mongo
    import pandas as pd

    if request.method == "GET":
        return render_template("/bulk/upload.html")
    if request.method == "POST":
        try:
            f = request.files['file']
            db=mongo.db
            df = pd.read_csv(f)
            data = df.to_dict(orient="records")
            for val in data:
                try:
                    val = bulk_mapping(val)
                    val['created_time'] = datetime.now()
                    val['source'] = 'bulk_upload'
                    db.bulk_leads.insert_one(val)
                    result = lead.apply_async(kwargs=val, queue="bulk_upload")
                except:
                    pass
        except:
            pass
        return redirect('http://automation.example.com/bulk_leads_list')
