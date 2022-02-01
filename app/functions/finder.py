from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
import time
from pymongo import MongoClient
from importlib import import_module

from app.functions import akshaya

def function_finder(lead_data):
    try:
        CONN=MongoClient("mongodb://REDACTED_MONGO_URI")
        DB = CONN['lead_automation']
        LEADS=DB['leads']
        SITE=DB['Site']
        print(SITE)
        print("db working")
        
    except Exception as e:
        print("Error occured due to "+str(e))
    
    try:
       
        project_name=lead_data.get("project_enquired_for")
        print("working before using db")
        site=SITE.find_one({"key_words":{"$in":["Akshaya Tango"]}})
        # site=SITE.find_one({"key_words":{"$in":["Akshaya Tango"]}}) 
        print("site name :",site," ",)
    
        globals()[site["name"]].addlead(site['name'],sub_project_name=project_name,**lead_data)
        
        return "success"
    except:
        print("error occured in function_finder")
        return "failed"