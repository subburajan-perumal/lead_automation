import logging
from urllib import response
from celery.result import AsyncResult
from flask import Blueprint, Response, jsonify, request

from config import Config
from ..util.request_handler import find_format
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
    return {"message":"99 acres endpoint working"}



@home.post("/99acres")
def webhook_99acres():
    try:
        logging.info(msg="request received")
        logging.info(msg=request.headers)
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


@home.get("/magicbricks")
def get_magicbricks():
    return {"message":"magicbricks endpoint working"}



@home.post("/magicbricks")
def webhook_magicbricks():
    try:
        logging.info(msg="request received")
        logging.info(msg=request.headers)
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
    return {"message":"housing endpoint working"}



@home.post("/housing")
def webhook_housing():
    try:
        logging.info(msg="request received")
        logging.info(msg=request.headers)
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
