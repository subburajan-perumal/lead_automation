import json
import logging
from datetime import datetime, time as dtime

import pytz
from bson import json_util
from flask import Blueprint, jsonify, render_template, request

from app.database import mongo


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s',
    encoding='utf-8'
    )

IST = pytz.timezone("Asia/Kolkata")

# blueprint for the app route
lead = Blueprint("lead", __name__, url_prefix="/lead")


def _format_timestamp(value):
    raw = value.get('$date') if isinstance(value, dict) else value
    try:
        parsed = datetime.strptime(str(raw).split(".")[0].replace("Z", ""), "%Y-%m-%dT%H:%M:%S")
    except ValueError:
        return str(raw)
    return parsed.strftime("%d/%m/%Y %H:%M:%S")


def _lead_fields(lead_row):
    """Top-level lead fields with timestamps made readable, without the project list."""
    detail = {key: value for key, value in lead_row.items() if key != 'project'}
    for key in ('created_at', 'modified_time'):
        if key in detail:
            detail[key] = _format_timestamp(detail[key])
    return detail


@lead.get("/all")
def leads_all():
    """One row per (lead, project) registration attempt, newest leads first."""
    try:
        lead_all = mongo.db.leads.find({"project": {"$exists": True}}, {"_id": 0}).sort("_id", -1).limit(100)
        leads_details = []
        for lead_row in json.loads(json_util.dumps(lead_all)):
            for project in lead_row.get('project') or []:
                lead_detail = _lead_fields(lead_row)
                lead_detail.update(project)
                if 'applied_time' in project:
                    lead_detail['applied_time'] = _format_timestamp(project['applied_time'])
                leads_details.append(lead_detail)
        return render_template("/lead/leads.html", data=leads_details)
    except Exception as e:
        logging.exception("could not list leads")
        return str(e), 500


@lead.get("/today")
def lead_today():
    """Leads modified today (IST), one row per lead with its projects and matched keywords."""
    try:
        start_of_day = IST.localize(datetime.combine(datetime.now(IST).date(), dtime.min))
        lead_all = mongo.db.leads.find(
            {"project": {"$exists": True}, "modified_time": {"$gte": start_of_day}},
            {"_id": 0},
        ).sort("_id", -1).limit(50)
        leads_details = []
        for lead_row in json.loads(json_util.dumps(lead_all)):
            projects = lead_row.get('project') or []
            lead_detail = _lead_fields(lead_row)
            lead_detail['project'] = sorted({p['subproject'] for p in projects if p.get('subproject')})
            lead_detail['match_keywords'] = sorted({k for p in projects for k in p.get('match_keywords') or []})
            lead_detail['project_list'] = ','.join(lead_detail['project'])
            leads_details.append(lead_detail)
        return render_template("/lead/view.html", data=leads_details)
    except Exception as e:
        logging.exception("could not list today's leads")
        return str(e), 500


@lead.get("/error_retry")
def error_retry():
    return render_template('/lead/error_retry.html')


@lead.post("/error_retry")
def getvalue():
    from app.functions.error_site_base import SiteAutomator1

    projectname = request.form.get('projectname', '').strip()
    phone_no = request.form.get('phone_no', '').strip()
    lead_id = request.form.get('lead_id', '').strip()
    logging.info("error retry requested: project=%s lead_id=%s", projectname, lead_id)
    if not (projectname and phone_no and lead_id):
        return jsonify({"Status": "Error", "Error": "projectname, phone_no and lead_id are all required"}), 400

    site_data = mongo.db.Site.find_one({"project_list.project_name": projectname})
    if site_data is None:
        return jsonify({"Status": "Error", "Error": "no site has a project named '{}'".format(projectname)}), 404
    lead_data = mongo.db.leads.find_one({'phone': phone_no})
    if lead_data is None:
        return jsonify({"Status": "Error", "Error": "no lead with phone {}".format(phone_no)}), 404

    browserAutomation = None
    try:
        browserAutomation = SiteAutomator1(
                                        phone=lead_data["phone"],
                                        email=lead_data["email"],
                                        lead_data=lead_data,
                                        match_keywords=[],
                                        site_data=site_data,
                                        sub_project_name=projectname,
                                        lead_id=lead_id
                                        )
        # automated_flow records the result and uploads the screenshots itself.
        browserAutomation.automated_flow()
    except Exception as e:
        logging.exception("error retry failed")
        return jsonify({"Status": "Error", "Error": str(e)}), 500
    finally:
        if browserAutomation is not None:
            browserAutomation.teardown()

    return render_template("/lead/error_retry_output.html")
