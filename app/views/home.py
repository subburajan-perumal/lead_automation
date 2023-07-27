from datetime import datetime
import json
import logging
import time

from bson import json_util
from celery.result import AsyncResult
from flask import Blueprint, Response, jsonify, redirect, render_template, request, url_for

from app.database import mongo
from app.tasks import bulk_lead, celery_app, lead
from app.util.request_handler import find_format
from app.util.utility import bulk_mapping


logging.basicConfig(
    level=logging.INFO,
    encoding='utf-8'
    )


# blueprint for the app route
home = Blueprint("home", __name__)


@home.get("/tasks/<task_id>")
def get_status(task_id):
    task_result = AsyncResult(task_id, app=celery_app)
    result = {
        "task_id": task_id,
        "task_status": task_result.status,
    }
    return jsonify(result), 200


@home.route("/test")
def test_page():
    return "site working"


@home.post("/")
def homepage_post():
    try:
        logging.info(msg="request received")
        start_time = time.time()
        data = find_format(request)
        if not data:
            return Response("invalid request", 200)
        if isinstance(data, dict):
            data['source'] = "zoho"
            lead.apply_async(kwargs=data, queue="lead")
            logging.info("lead %s queued", data.get("lead_id"))
        logging.info(f"Response time {time.time() - start_time}")
        return Response("received", 200)

    except Exception:
        logging.exception("invalid request received")
        return Response("something went wrong\n", status=400)


def retry_mapping(lead_request):
    return {
        'interested_properties': lead_request['subproject'],
        'email': lead_request['email'],
        'name': lead_request['name'],
        'phone': lead_request['phone'],
        'lead_id': lead_request.get('lead_id'),
        'source': 'retry',
    }


@home.post("/retry_leads")
def webhook_retry():
    try:
        logging.info(msg="retry_leads request received")
        data = request.get_json(silent=True)
        if not isinstance(data, dict) or not all(k in data for k in ('subproject', 'email', 'name', 'phone')):
            return Response("invalid request", 200)
        lead.apply_async(kwargs=retry_mapping(data), queue="lead")
        return Response("received", 200)

    except Exception:
        logging.exception("invalid request received")
        return Response("something went wrong\n", status=400)


def _format_timestamp(value):
    raw = value.get('$date') if isinstance(value, dict) else value
    try:
        parsed = datetime.strptime(str(raw).split(".")[0].replace("Z", ""), "%Y-%m-%dT%H:%M:%S")
    except ValueError:
        return str(raw)
    return parsed.strftime("%d/%m/%Y %H:%M:%S")


# UPLOAD

@home.route('/bulk_leads_list')
def bulk_leads():
    try:
        cur = mongo.db["bulk_leads"].find({'source': 'bulk_upload'}).sort("_id", -1).limit(50)
        leads_details = []
        for bulk_row in json.loads(json_util.dumps(cur)):
            bulk_row['phone'] = str(bulk_row.get('phone', ''))[1:]
            if 'created_time' in bulk_row:
                bulk_row['created_time'] = _format_timestamp(bulk_row['created_time'])
            leads_details.append(bulk_row)

        return render_template('/bulk/list.html', x=leads_details)
    except Exception as e:
        logging.exception("could not list bulk leads")
        return jsonify({"Status": "Error", "Error": str(e)})


# UPLOAD BULK CSV

@home.route("/bulk_upload", methods=["GET", "POST"])
def uploader_file():
    import pandas as pd

    if request.method == "GET":
        return render_template("/bulk/upload.html")

    logging.info(msg="Bulk upload request received")
    try:
        df = pd.read_csv(request.files['file'])
    except Exception:
        logging.exception("could not read the uploaded CSV")
        return Response("Could not read the uploaded file. Upload a CSV with the bulk lead columns.", status=400)

    queued = failed = 0
    for row_number, row in enumerate(df.to_dict(orient="records"), start=2):
        try:
            lead_data = bulk_mapping(row)
            lead_data['source'] = 'bulk_upload'
            record = dict(lead_data, created_time=datetime.now())
            mongo.db.bulk_leads.update_one(
                {'phone': record['phone']},
                {'$set': record},
                upsert=True
            )
            bulk_lead.apply_async(kwargs=lead_data, queue="bulk")
            queued += 1
        except Exception:
            failed += 1
            logging.exception("bulk upload: skipped CSV row %s", row_number)
    logging.info("bulk upload: %s queued, %s skipped", queued, failed)
    return redirect(url_for('home.bulk_leads'))
