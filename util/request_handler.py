import imp
import json
from flask import request

###post request-> P_request
def find_format(P_request):
    print("fomat finder working")
    content_type=P_request.headers['Content-type']
    data={}
    if "x-www-form-urlencoded" in content_type:
            print("default post request")   
            data =P_request.get_data()

    elif "form-data" in content_type:
        tempdata=P_request.get_data()
        data=json.loads(tempdata.decode())
    
    elif "json" in content_type:
        if(type(P_request.get_json()) is dict):
            data=P_request.get_json()
        #multiple json in single request
        elif(type(P_request.get_json())==list):
            print("json array")
            data=P_request.get_json()
    else:
        data={}
    return data
