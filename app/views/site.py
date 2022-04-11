"""
website routing
"""
import os

# from bson.objectid import ObjectId
# from bson.json_util import dumps as bson_dumps
from flask import Blueprint, request, render_template
from pymongo import MongoClient
from wtforms import Form, StringField, URLField
from wtforms import validators
from bson.json_util import dumps


site = Blueprint("site", __name__, url_prefix="/site", template_folder="")


mongocursor = MongoClient(os.getenv("MONGO_DB"))
db = mongocursor['lead_automation']


class SiteForm(Form):
    """
    this class contain the form fields
    Args:
        Form (class): this class is wtfform
    """
    f_sitename = StringField(
        label="Site name",
        validators=[validators.DataRequired("please enter the sitename")]
    )
    f_uri = URLField(label="site_url")


@site.route("/test")
def site_test():
    message="site working"
    return render_template("/site/message.html",message=message)

@site.route("/")
def view_site():
    """
    this method is route for site operation
    Returns:
        html: this load page from site view
    """
    print("view site working")
    data=""
    try:
        data=db.Site.aggregate(
            [
                {
                    "$project":
                    {   
                        "name":1,
                        "status":1,
                        "projectlist":{"$size":["$project_list"]}
                    }
                },
                {
                    "$sort":
                        {"name":1}
                }
            ]
        )
        # data=dumps(data)
        
        
    except Exception as e:
        print("exception occured")
        print(str(e))
    # for i in data:
    #     print(i)

    return render_template("site/view_site.html",data=data)


@site.route("/add")
def site_add():
    """
    this method is route for add a site and other detail

    Returns:
        html: show the form for add the site
    """
    print("site route working")
    form=SiteForm()
    return render_template("site/addsite.html", form=form)
    
    # return Response{"internal error",404}



@site.post("/add")
def add_to_db():
    """
    Handle the post request from the route /add
    Returns:
        html: acknowledgement of the post request
    """
    try:
        form_value = request.form.to_dict()
        print(form_value)
        form_name = form_value.get("site_name", "")
        form_uri = form_value.get("uri", "")
        form_sitedata = form_value.get("sitedata", "")

        form_projectlist = form_value.get("projectlist", "")

        print(form_name, form_uri, form_sitedata, form_projectlist, sep="\n")
       
        return render_template("site/message.html", message="sumbitted data")

    except Exception as d_exception:
        print("error occured")
        print(str(d_exception))
        return render_template("site/message.html", message="failed")
        # db.Site.insert_one()


@site.get("/site/<site_name>")
def find_site(site_name):
    site_detail=db.Site.find_one({"name":site_name})
    return render_template("meassage",message=site_detail)

# @site.get("/delete")
# def site_delete_page():
#     data = db.testSite.find()
#     return render_template("/site/delete.html", data=data)


# @site.route("/site/")
# def site_route():
#     """route for site details

#     Returns:
#         html: view the site name in the database
#     """
#     print("site route2 working")
#     return render_template("base.html")


# @site.route("/update")
# def site_update_page():
#     data = list(db.Site.find())
#     json_data = bson_dumps(data)
#     print(json_data)
#     return render_template("/site/update.html", data=json_data)


# @site.post("/update")
# def site_update():
#     update_id = request.form['update_name']
#     if update_id == "":
#         return render_template("/site/message.html", message="nothing selected")
#     result = db.testSite.delete_one({"_id": ObjectId(update_id)})
#     print("site route working")

#     message = "updated"
#     return render_template("/site/message.html", message=message)


# @site.route("/delete")
# def site_delete_page():
#     """show the list of sitename for deletion

#     Returns:
#         html:view the sitename in database
#     """
#     data = db.testSite.find()
#     return render_template("/site/delete.html", data=data)


# @site.post("/delete")
# def site_delete():
#     """
#     Handle the delete request
#     Returns:
#         html: "delete thee sitename from database"
#     """
#     try:
#         delete_id = request.form['delete_name']
#         print(delete_id)
#         if delete_id == "":
#             return render_template("/site/message.html", message="nothing selected")
#         result = db.testSite.delete_one({"_id": ObjectId(delete_id)})
#         print(result.raw_result)
#         print(result.acknowledged)
#         print(result.deleted_count)
#         return render_template("/site/message.html", message="deleted")

#     except Exception as d_exception:
#         print(str(d_exception))
#         return render_template("/site/message.html", message="failed")
