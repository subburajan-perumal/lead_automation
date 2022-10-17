from flask import Flask, render_template, request,jsonify
import pymongo
from pymongo import MongoClient
import json
from datetime import datetime
from json import loads
from app.functions.site_base import SiteAutomator

app = Flask (__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/error_retry", methods=["GET","POST"])
def getvalue():
    if request.method == "POST":
        projectname = request.form['projectname']
        phone_no = request.form['phone_no']
        print(projectname, phone_no)
        try:
            MONGO_DB = "REDACTED"
            CONN = MongoClient(MONGO_DB)
            DB = CONN['lead_automation']

            #site_data

            site_data = DB.Site.find_one({"project_list.project_name": projectname})
            print(site_data)
            print("site data fetched successfully")

            #lead_data

            lead_data  = DB.leads.find_one({'phone': phone_no})
            print(lead_data)
            print("lead data fetched successfully")

            site_name = site_data['name']
            site_projectname = projectname
            browserAutomation = SiteAutomator(  
                                            phone = lead_data["phone"],
                                            email= lead_data["email"],
                                            lead_data= lead_data,
                                            match_keywords= None,
                                            site_data= site_data
                                            )
            browserAutomation.projectCheck(site_name, site_projectname)
            print("browser automation worked for error retry successfully")
            browserAutomation.automated_flow()
            browserAutomation.upload_data()
            browserAutomation.teardown()
        
        
        
        except Exception as e:
            return jsonify({"Status": "Error", "Error": str(e)})


    return 'data collected'


if __name__ == '__main__':
    app.run()