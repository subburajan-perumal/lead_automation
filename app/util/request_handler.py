import json
import logging

from flask import Request

from config import required_field


def find_format(P_request: Request):
    """Read a Zoho webhook body (JSON or form-encoded) into a lead dict.

    Returns {} when the body can't be read or is missing any of config.required_field.
    """
    try:
        content_type = P_request.content_type or ""

        if "json" in content_type:
            req_data = P_request.get_json(silent=True)
        elif "x-www-form-urlencoded" in content_type or "multipart/form-data" in content_type:
            req_data = P_request.form.to_dict()
        else:
            # Some Zoho webhook configurations post JSON with a text/plain content type.
            req_data = json.loads(P_request.get_data(as_text=True) or "{}")

        if not isinstance(req_data, dict):
            return {}
        if all(req_data.get(field) not in (None, "") for field in required_field):
            return req_data
        logging.info("request missing required fields: %s",
                     [field for field in required_field if req_data.get(field) in (None, "")])
        return {}

    except Exception:
        logging.exception("problem in finding data type")
        return {}
