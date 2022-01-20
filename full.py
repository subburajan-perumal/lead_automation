
from flask import Flask,request,Response
import queue
app=Flask(__name__)

request_queue=queue.PriorityQueue(50)

def queue_request(request_data,priority):
    print(request_queue.qsize())
    request_queue.put((priority,request_data))
    while request_queue.qsize()!=0:
        print(f"{request_queue.qsize()} {request_queue.get()}")


@app.post('/')
def webhook():
    queue_request(priority=5,request_data=request.headers)
    # print(request.headers)
    return Response("Success",status=200)


if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True, port = 8686)
