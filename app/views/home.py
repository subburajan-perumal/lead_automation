from urllib import response
from flask import Blueprint,Response,request
from ..util.request_handler import find_format
import time
import json
from app.tasks import lead
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
async def home_page():
    try:
        start_time=time.time()
        data={}
        data=find_format(request)
        if data=={}: return Response("invalid request",200)
        if type(data) is list:
            print(data)
        
        elif type(data) is dict:
            print(data)
            taskid=lead.apply_async(kwargs=data)   
            print("task executed succesfully")      
        
        else:
            print(data)
       
        end_time=time.time()
       
        print(f"Response time {end_time-start_time}")
        return Response("success",status=200)     
        

    except Exception as e:
        print(str(e))
        return Response("something went wrong\n",status=400)


