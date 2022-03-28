from flask import Blueprint,request,Response,render_template
from bson.objectid import ObjectId
from bson.json_util import dumps as bson_dumps
from pymongo import MongoClient
import os
import json   

site=Blueprint("site",__name__,url_prefix="/site",template_folder="")


mongocursor=MongoClient(os.getenv("MONGO_DB"))
db=mongocursor['lead_automation']

@site.get("/")
def view_site():
    print("view site working")
    return render_template("site/view_site.html")

@site.get("/add")
def site_data():
    print("site route working")
    data= db.Site.find()
    return render_template("site/addsite.html",data=data)


@site.post("/add")
def add_to_db():
    try:
        site_data=request.form['others']
        if site_data != "":
            print(type(site_data))
            site_data=dict(json.loads(site_data))
            if "name" in site_data and "url" in site_data:
                
                inserted=db.testSite.insert_one(site_data)
                print(inserted.inserted_id)
                return render_template("site/message.html" ,message="Site")

        # print(request.form.to_dict())
        # form_data=request.form.to_dict()
        # if form_data['site_name'] != "":
        #     fname=form_data["site_name"]
        #     furl=form_data['url']
        #     other_data="" 
        #     if form_data['others'] != "":
        #         other_data=json.loads(form_data['others'])
            
        #     print(type(other_data))
        #     existingproject=db.testSite.find_one({"name":fname})
        #     if existingproject  :
        #         return render_template("site/message.html",message="site already exist")

            # final={"name":fname,"url":furl,"site_data":other_data}
        
        #     print(id)
        return render_template("site/message.html" ,message="invalid data")

    except Exception as e:
        print(str(e))
        return render_template("site/message.html" ,message="failed")
        # db.Site.insert_one()
    


@site.route("/site/")
def site_route():
    print("site route2 working")
    return render_template("base.html")

@site.get("/update")
def site_update_page():
    data= list(db.Site.find())
    json_data=bson_dumps(data)
    print(json_data)
    return render_template("/site/update.html",data=json_data)


@site.post("/update")
def site_update():
    update_id=request.form['update_name']
    if update_id =="":
            return render_template("/site/message.html",message="nothing selected")
    result=db.testSite.delete_one({"_id":ObjectId(update_id)})
    print("site route working")

    message="updated"
    return render_template("/site/message.html",message=message)


@site.get("/delete")
def site_delete_page():
    data= db.testSite.find()
    return render_template("/site/delete.html",data=data)

@site.post("/delete")
def site_delete():
    try:
        delete_id=request.form['delete_name']
        print(delete_id)
        if delete_id =="":
            return render_template("/site/message.html",message="nothing selected")
        result=db.testSite.delete_one({"_id":ObjectId(delete_id)})
        print(result.raw_result)
        print(result.acknowledged)
        print(result.deleted_count)
        return render_template("/site/message.html",message="deleted")
    except:
        return render_template("/site/message.html",message="failed")