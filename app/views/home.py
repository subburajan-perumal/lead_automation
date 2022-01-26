from flask import Blueprint,Response,request
from markupsafe import re
from util.request_handler import find_format
import time
import json
from tasks import CELERY
# from .. import tasks

#blueprint for the app route
home=Blueprint("home",__name__)

@home.get("/tasks/")
def task_response():
    taskid=request.args.get('taskid')
    return Response(taskid,200)
@home.route("/test")
def test_page():
    return "site working"

@home.post("/")
def home_page():
    try:
        start_time=time.time()
        print(request.headers)
        # print(request.is_json)
        data=find_format(request)
        if type(data) is list:
            print(data)
            #need to work
            # taskid=CELERY.send_task("tasks.bulk_lead",kwargs=data) 
        
        elif type(data) is dict:
            print(data)
            taskid=CELERY.send_task("tasks.lead",kwargs=data)   
            print("task executed succesfully")       
        else:
            print(data)
       
        end_time=time.time()

        print(f"Response time {end_time-start_time}")
        return Response(str(taskid),status=200)     
        

    except Exception as e:
        print(str(e))
        return Response("something went wrong\n",status=400)


