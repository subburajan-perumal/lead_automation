from flask import Flask,request,Response
from util.request_handler import find_format
import logging
import queue
import time

from test.test import add_request 

app=Flask(__name__)


request_queue=queue.PriorityQueue(500)
logging.basicConfig(level=logging.DEBUG,filename="system.log")
# async def execution_queue():
#     global on_execution
#     on_execution=True
#     print("Execution queue started at ")
#     time.sleep(5)
#     while request_queue.qsize()!=0:
#         data =request_queue.get()
#         time.sleep(5)
#         print(data[1])
#     on_execution=False
#     print("Execution ended")

# async def add_request(priority,request_data):
#     print(request_queue.qsize())
    
#     if on_execution==False:
#         print("adding request to empty queue ")
#         request_queue.put((priority,request_data))
#         print("request added to queue")
#         print(request_queue.queue)
#     if on_execution==True:
#         request_queue.put((priority,request_data))
    
    
#     # while request_queue.qsize()!=0:
#     #     print(f"{request_queue.qsize()} {request_queue.get()}")

@app.post('/')
def webhook():
    try:
        start_time=time.time()
        data=find_format(request)
        if data is list:pass
        elif type(data) is dict:
            print(data)        
        end_time=time.time()
        # logging.info(f"{time.asctime}request received ")
        print(f"Response time {end_time-start_time}")     
        return Response(str(request_queue.qsize()),status=200)

    except Exception as e:
        print(str(e))
        return Response("something went wrong\n",status=400)
    


if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True, port = 8686,threaded=True)
