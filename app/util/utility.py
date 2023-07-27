from datetime import datetime
import math
import os
from uuid import uuid4

import phonenumbers as PN
import pytz
import redis
import requests
from celery.utils.log import get_task_logger

from config import Config


celery_logger = get_task_logger(__name__)

ZOHO_TOKEN_CACHE_KEY = "lead_automation:zoho_access_token"
HTTP_TIMEOUT = 30


def cmpstring(string1, string2):
    str1 = "".join([i for i in string1 if i.isalpha()])
    str2 = "".join([i for i in string2 if i.isalpha()])
    return str1 == str2


def getTime():
    IST = pytz.timezone("Asia/Kolkata")
    return datetime.now(IST)


def isValidPhoneNumber(phone_number) -> bool:
    return PN.is_possible_number(phone_number)


def getPhonenumber(numberlist: list):
    """Return the first possible phone number in the list, in E.164 format, else None.

    Missing fields and unparseable values are skipped instead of failing the whole lead.
    """
    for number in numberlist:
        if number is None or str(number).strip() == "":
            continue
        try:
            parsed = PN.parse(str(number), region="IN")
        except PN.NumberParseException:
            continue
        if isValidPhoneNumber(parsed):
            return PN.format_number(parsed, PN.PhoneNumberFormat.E164)
    return None


def getName(name):
    """Split a full name into (first, last). Single names are used for both."""
    parts = str(name or "").split()
    if not parts:
        return "", ""
    if len(parts) == 1:
        return parts[0], parts[0]
    return " ".join(parts[:-1]), parts[-1]


# pre_akshaya_Adityaram_phase_5_krishnamoorthy perumal.png
# (site,sub_projectname,path,leadname)


def getsavePath(path, path2, site_name, sub_project_name, leadname, phone):
    from app.database import get_db

    # The Zoho copy of each screenshot is named after the project's filename alias, if it has one.
    subname = sub_project_name
    try:
        site = get_db()["Site"].find_one({"project_list.project_name": sub_project_name})
        for elem in (site or {}).get("project_list", []):
            if elem.get("project_name") == sub_project_name and elem.get("filename"):
                subname = elem["filename"]
                break
    except Exception:
        celery_logger.exception("could not look up the project filename; using the project name")

    lead_part = "{}_{}_{}_{}".format(site_name, sub_project_name, str(leadname).replace(" ", "_"), phone)
    return [
        "{}/pre_{}.png".format(path, lead_part),
        "{}/post_{}.png".format(path, lead_part),
        "{}/err_{}.png".format(path, lead_part),
        "{}/pre_{}_{}.png".format(path2, subname, uuid4().hex),
        "{}/post_{}_{}.png".format(path2, subname, uuid4().hex),
        "{}/err_{}_{}.png".format(path2, subname, uuid4().hex),
    ]


# MAPPING BULK DATA


def _is_blank(value):
    return value is None or (isinstance(value, float) and math.isnan(value)) or str(value).strip() == ""


def bulk_mapping(data):
    phone = data["Phone"]
    # pandas reads a phone column as float (919876543210.0), which then fails to parse.
    if isinstance(phone, float) and phone.is_integer():
        phone = int(phone)
    phone = str(phone).strip()
    if not phone.startswith("+"):
        phone = "+" + phone

    email = data.get("Email")
    if _is_blank(email):
        email = phone + "@example.com"

    return {
        "lead_id": str(data["LEADID"])[5:],
        "email": email,
        "phone": phone,
        "mobile": phone,
        "alt_phone": phone,
        "name": data["Full Name"],
        "project_enquired_for": "" if _is_blank(data.get("Project Enquired for")) else data["Project Enquired for"],
        "interested_properties": "" if _is_blank(data.get("Interested Properties")) else data["Interested Properties"],
    }


# SEND MAIL VIA MAILGUN


def send_mail(lead_id, path, sub_project_name, name1):
    """Email the automation team about a failed registration, with the screenshot attached.

    Uses the Mailgun HTTP API directly. Lead names come from outside the system, so they
    must never be interpolated into a shell command.
    """
    if not (Config.MAILGUN_API_KEY and Config.MAILGUN_DOMAIN and Config.MAILGUN_TO):
        celery_logger.warning("Mailgun is not configured; skipping failure email for lead %s", lead_id)
        return None

    subject = "Error. {} - {}".format(name1, sub_project_name)
    text = "Error. Lead registration failure. Lead ID: {} Project: {} Name: {}".format(
        lead_id, sub_project_name, name1
    )
    data = {
        "from": "Automation Error <mailgun@{}>".format(Config.MAILGUN_DOMAIN),
        "to": Config.MAILGUN_TO,
        "subject": subject,
        "text": text,
    }
    try:
        if path and os.path.isfile(path):
            with open(path, "rb") as attachment:
                response = requests.post(
                    "https://api.mailgun.net/v3/{}/messages".format(Config.MAILGUN_DOMAIN),
                    auth=("api", Config.MAILGUN_API_KEY),
                    data=data,
                    files=[("attachment", (os.path.basename(path), attachment, "image/png"))],
                    timeout=HTTP_TIMEOUT,
                )
        else:
            response = requests.post(
                "https://api.mailgun.net/v3/{}/messages".format(Config.MAILGUN_DOMAIN),
                auth=("api", Config.MAILGUN_API_KEY),
                data=data,
                timeout=HTTP_TIMEOUT,
            )
        response.raise_for_status()
        return response.status_code
    except requests.RequestException:
        celery_logger.exception("failed to send failure email for lead %s", lead_id)
        return None


# ZOHO ACCESS TOKEN


def _redis():
    return redis.Redis.from_url(Config.REDIS_URL)


def refresh_access_token():
    """Exchange the Zoho refresh token for a new access token and cache it in Redis."""
    response = requests.post(
        "{}/oauth/v2/token".format(Config.ZOHO_ACCOUNTS_URL),
        params={
            "client_id": Config.ZOHO_CLIENT_ID,
            "client_secret": Config.ZOHO_CLIENT_SECRET,
            "refresh_token": Config.ZOHO_REFRESH_TOKEN,
            "grant_type": "refresh_token",
        },
        timeout=HTTP_TIMEOUT,
    )
    response.raise_for_status()
    payload = response.json()
    access_token = payload.get("access_token")
    if not access_token:
        raise RuntimeError("Zoho token refresh failed: {}".format(payload.get("error", "no access_token in response")))

    # Zoho tokens live for an hour; expire the cached copy five minutes early.
    ttl = max(int(payload.get("expires_in", 3600)) - 300, 60)
    try:
        _redis().set(ZOHO_TOKEN_CACHE_KEY, access_token, ex=ttl)
    except redis.RedisError:
        celery_logger.warning("could not cache the Zoho access token in Redis")
    return access_token


def get_access_token():
    try:
        cached = _redis().get(ZOHO_TOKEN_CACHE_KEY)
        if cached:
            return cached.decode("utf-8")
    except redis.RedisError:
        celery_logger.warning("Redis unavailable; requesting a fresh Zoho access token")
    return refresh_access_token()


def _zoho_request(method, path, **kwargs):
    """Call the Zoho CRM API, refreshing the access token once if Zoho rejects it."""
    url = "{}{}".format(Config.ZOHO_API_URL, path)
    headers = kwargs.pop("headers", {})
    for attempt in range(2):
        token = get_access_token() if attempt == 0 else refresh_access_token()
        headers["Authorization"] = "Zoho-oauthtoken {}".format(token)
        response = requests.request(method, url, headers=headers, timeout=HTTP_TIMEOUT, **kwargs)
        if response.status_code != 401:
            return response
    return response


# UPLOAD ATTACHMENT TO ZOHO


def upload_an_attachment(lead_id, path):
    if not lead_id:
        celery_logger.warning("no Zoho lead id; not uploading %s", path)
        return None
    if not os.path.isfile(path):
        celery_logger.warning("screenshot %s does not exist; nothing to upload", path)
        return None

    # Drop the uuid suffix so the attachment shows a readable name in Zoho.
    root, ext = os.path.splitext(os.path.basename(path))
    filename = root.rsplit("_", 1)[0] + ext
    try:
        with open(path, "rb") as screenshot:
            response = _zoho_request(
                "POST",
                "/crm/v2/Leads/{}/Attachments".format(lead_id),
                files=[("file", (filename, screenshot, "image/png"))],
            )
        celery_logger.info("attachment upload for lead %s: HTTP %s", lead_id, response.status_code)
        return response.status_code
    except Exception:
        celery_logger.exception("failed to upload %s to Zoho lead %s", path, lead_id)
        return None


# SEARCH PROJECT ID


def _zoho_criteria_value(value):
    # Zoho search criteria treat these characters as syntax unless escaped.
    value = str(value)
    for char in ("\\", "(", ")", ","):
        value = value.replace(char, "\\" + char)
    return value


def getProjectID(project_name, access_token=None):
    """Zoho Deal id for a project name or alias, or {"error": ...} when there is no match."""
    name = _zoho_criteria_value(project_name)
    params = {
        "fields": "Deal_Name",
        "criteria": "(Deal_Name:starts_with:{0})or(Project_Alias_2:starts_with:{0})or(Project_Alias:starts_with:{0})".format(name),
    }
    response = _zoho_request("GET", "/crm/v2/Deals/search", params=params)

    # Zoho answers 204 with an empty body when nothing matches.
    if response.status_code == 200:
        data = response.json().get("data")
        if data:
            return data[0]["id"]

    return {"error": "No such project"}


# INSERT NEW RECORD IN ZOHO


def insert_records(record, access_token=None):
    request_body = {
        "data": [record],
        "duplicate_check_fields": ["Email", "Phone"],
        "trigger": ["workflow"],
    }
    response = _zoho_request("POST", "/crm/v2/Leads/upsert", json=request_body)
    return {"response": str(response.content), "status_code": response.status_code}
