from flask import Flask,request,Response
import queue

app=Flask(__name__)


request_queue=queue.PriorityQueue(50)
on_execution=False

def execution_queue():
    global on_execution
    on_execution=True
    print("Execution queue started")
    while request_queue.qsize()!=0:
        data =request_queue.get()
        print(data[1])
    on_execution=False


def add_request(priority,request_data):
    print(request_queue.qsize())
    
    if on_execution==False:
        print("adding request to empty queue ")
        request_queue.put((priority,request_data))
        print("request added to queue")
        print(request_queue.queue)
        execution_queue()
        print("execution queue triggered")
    if on_execution==True:
        request_queue.put((priority,request_data))
    
    
    # while request_queue.qsize()!=0:
    #     print(f"{request_queue.qsize()} {request_queue.get()}")

@app.post('/')
def webhook():
    try:
        print(request.headers)
        print(f"data :{request.get_data()}\ntype : {type(request.get_data())}")
        print(f"\ndata :{request.get_json()} \ntype: {type(request.get_json())}")
        # add_request(4,request.get_json())

        
        #single json request
        if(type(request.get_json())==dict):
            add_request(priority=4,request_data=request.get_json())
        
        #multiple json in single request
        elif(type(request.get_json())==list):
            for data in request.get_json():
                add_request(priority=5,request_data=data)
        # # print(request.headers)
        # # print(request.get_json())
        # print(type(request.get_json()))
        return Response("Success",status=200)

    except:
        return Response("something went wrong",status=400)
    


if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True, port = 8686,threaded=True)
