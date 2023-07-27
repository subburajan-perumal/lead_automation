"""
website routing
"""
import json
import logging

from flask import Blueprint, request, render_template
from wtforms import Form, StringField, URLField
from wtforms import validators

from app.database import mongo


site = Blueprint("site", __name__, url_prefix="/site", template_folder="")


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
    message = "site working"
    return render_template("/site/message.html", message=message)


@site.route("/")
def view_site():
    """
    this method is route for site operation
    Returns:
        html: this load page from site view
    """
    data = []
    try:
        data = list(mongo.db.Site.aggregate(
            [
                {
                    "$project":
                    {
                        "name": 1,
                        "status": 1,
                        "projectlist": {"$size": {"$ifNull": ["$project_list", []]}}
                    }
                },
                {
                    "$sort":
                        {"name": 1}
                }
            ]
        ))
    except Exception:
        logging.exception("could not list sites")

    return render_template("site/view_site.html", data=data)


@site.route("/add")
def site_add():
    """
    this method is route for add a site and other detail

    Returns:
        html: show the form for add the site
    """
    form = SiteForm()
    return render_template("site/addsite.html", form=form)


def _json_field(form_value, key, default):
    raw = form_value.get(key, "").strip()
    return json.loads(raw) if raw else default


@site.post("/add")
def add_to_db():
    """
    Handle the post request from the route /add: store a new builder site.
    Site data is a JSON object (merged into the site document, e.g. login details);
    project list is a JSON array of projects, each with project_name and keywords.
    Returns:
        html: acknowledgement of the post request
    """
    form_value = request.form.to_dict()
    name = form_value.get("site_name", "").strip()
    if not name:
        return render_template("site/message.html", message="site name is required"), 400
    try:
        site_data = _json_field(form_value, "sitedata", {})
        project_list = _json_field(form_value, "projectlist", [])
    except json.JSONDecodeError as error:
        return render_template("site/message.html", message="invalid JSON: {}".format(error)), 400
    if not isinstance(site_data, dict) or not isinstance(project_list, list):
        return render_template("site/message.html",
                               message="site data must be a JSON object and project list a JSON array"), 400
    if mongo.db.Site.find_one({"name": name}):
        return render_template("site/message.html", message="site '{}' already exists".format(name)), 409

    document = dict(site_data)
    document.update({
        "name": name,
        "url": form_value.get("uri", "").strip(),
        "status": 1,
        "project_list": project_list,
    })
    mongo.db.Site.insert_one(document)
    return render_template("site/message.html", message="site '{}' added".format(name))


@site.get("/<site_name>")
def find_site(site_name):
    site_detail = mongo.db.Site.find_one({"name": site_name}, {"_id": 0})
    if site_detail is None:
        return render_template("site/message.html", message="no site named '{}'".format(site_name)), 404
    return render_template("site/message.html", message=site_detail)
