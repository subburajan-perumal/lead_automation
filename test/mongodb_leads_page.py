import json
from bson import json_util
from pymongo import MongoClient


MONGO_DB="REDACTED"

CONN = MongoClient(MONGO_DB)
DB = CONN['lead_automation']
lead_all = DB.leads.find({"project":{"$exists":"true"}},{"_id":0}).sort("_id",-1).limit(50)
lead_all=json.loads(json_util.dumps(lead_all))
leads_details = []

for lead in lead_all:
    lead_detail = dict()
    for key, value in lead.items():
        if key != 'project' and key != 'created_at':
            lead_detail[key] = value
        if key == 'created_at':
            lead_detail[key] = value['$date']
        if key == 'modified_time':
            lead_detail[key] = value['$date']
        arr = []
        if key == 'project':
            for project in value:
                arr.append(project['subproject'])
            lead_detail[key] = arr     
    print(lead_detail)
print(leads_details)