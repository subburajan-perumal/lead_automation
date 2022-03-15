import json

from flask import Request
def find_format(P_request:Request):
    try:

        print("fomat finder working")
        content_type=P_request.content_type.split("/")
        req_data={}

        if "x-www-form-urlencoded" in content_type :
                print("default post P_request")
                print(P_request)   
                req_data =P_request.get_data()
                

        elif "form-data" in content_type:
            tempdata=P_request.get_data()
            req_data=json.loads(tempdata.decode())


        # elif "xml" in content_type :
        #     print("xml")
        #     tempdata=P_request.get_data()
        #     req_data=xmltodict.parse(tempdata)
        #     print(req_data)
            

        elif "json" in content_type:
            if(type(P_request.get_json()) is dict):
                req_data=P_request.get_json()
                if 'phone' in req_data and 'email' in req_data and 'lead_id'  in req_data and 'name' in req_data:
                    return req_data
                else:
                    req_data={}
                    print(req_data)
                # data=''.join(key for key,value in data if key.isalnum())
            #multiple json in single P_request
            elif(type(P_request.get_json())==list):
                print("json array")
                # for _ in P_request.get_json():

        else:
            req_data={}
        return req_data
    
    except:
        print("problem in finding data type")
        req_data={}
        return req_data
    