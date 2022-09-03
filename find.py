
import pymongo

client = pymongo.MongoClient("mongodb://REDACTED_MONGO_URI")
db = client["lead_automation"]
mycol = db["Site"]

project_name = db.mycol.find({},{"project_list":1})
print(project_name)

# def rename():
#     for i in db.mycol:
#         if site_projectname == project_name:
#             subname = db.mycol.find({},{"filename":1})

#         return[
#         str(str(path) + '/' + "pre" + "_" + str(subname)+ ".png"),
#         str(str(path) + '/' + "post" + "_" + str(subname)+ ".png"),
#         str(str(path) + '/' + "err" + "_" + str(subname)+ ".png")
#         ]

