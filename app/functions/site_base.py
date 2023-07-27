import os
import shutil
from datetime import datetime, timedelta

from celery.utils.log import get_task_logger
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service

from app.database import get_db
from app.functions.browser_automation import (
    adityaram, akshaya, alliance, arun_excello, brigade, casagrand, dlf, doshi, dra, fomra,
    gsquare, hiranandani, krishnagrp, lancor, lifestyle, pragnya, radiance, radiance_,
    shriram, sidharth, tvs, urban_tree, vr, xs, xs_real,
)
from app.util.utility import getTime, getsavePath, upload_an_attachment
from config import Config

logger = get_task_logger(__name__)

WEBDRIVER_LOG = "webdriver.log"

# Result codes a site function returns, stored as project.status on the lead.
RESULT_SKIPPED = 0    # already registered with this project inside the site's window
RESULT_SUCCESS = 1
RESULT_FAILED = 2
RESULT_PARTIAL = -1   # registered, but the site also showed an error

project_store = {
    "adityaram": adityaram,
    "alliance": alliance,
    "akshaya": akshaya,
    "brigade": brigade,
    "casagrand": casagrand,
    "dlf": dlf,
    "doshi": doshi,
    "dra": dra,
    "fomra": fomra,
    "gsquare": gsquare,
    "hiranandani": hiranandani,
    "krishnagrp": krishnagrp,
    "lifestyle": lifestyle,
    "lancor": lancor,
    "pragnya": pragnya,
    "radiance": radiance,
    "radiance_phase_2": radiance_,
    "sidharth": sidharth,
    "shriram": shriram,
    "tvs": tvs,
    "vijayaraja": vr,
    "xs": xs,
    "arun_excello": arun_excello,
    "urban_tree": urban_tree,
    "xs_real": xs_real
}
required_store = {
    "adityaram": {"function": adityaram, "required_field": ["phone", "email"]},
    "alliance": {"function": alliance, "required_field": ["phone"]},
    "akshaya": {"function": akshaya, "required_field": ["phone"]},
    "brigade": {"function": brigade, "required_field": ["email", "phone"]},
    "casagrand": {"function": casagrand, "required_field": ["phone"]},

    # country cod also need for dlf
    "dlf": {"function": dlf, "required_field": ["phone"]},
    "doshi": {"function": doshi, "required_field": ["phone"]},
    "dra": {"function": dra, "required_field": ["phone"]},
    "fomra": {"function": fomra, "required_field": ["email", "phone"]},
    "gsquare": {"function": gsquare, "required_field": ["email", "phone"]},

    # countrycode not required
    "hiranandani": {"function": hiranandani, "required_field": ["email", "phone"]},
    "krishnagrp": {"function": krishnagrp, "required_field": ["email"]}
}


class SiteAutomator:
    """Registers one lead on one builder's site with Firefox, then records the outcome.

    Subclasses change three things: whether screenshots go to Zoho, whether the
    "already registered recently" check applies, and whether Firefox runs headless.
    """

    upload_attachments = True
    skip_existing_check = False
    headless = Config.BROWSER_HEADLESS

    def __init__(self, phone, email, lead_data, match_keywords, site_data, lead_id=None) -> None:
        self.email = email
        self.phone = phone
        self.lead_data = lead_data
        self.lead_id = lead_id or lead_data.get("lead_id")
        self.path = ""
        self.automate_path = None
        self.result = RESULT_SKIPPED
        self.site_data = site_data
        self.match_keywords = match_keywords or []
        self.sub_project_name = None
        self.projectexist = False

        self.DB = get_db()
        self.LEAD = self.DB["leads"]

        opt = Options()
        opt.add_argument("--incognito")
        if self.headless:
            opt.add_argument("--headless")
        self.browser = webdriver.Firefox(
            options=opt,
            service=Service(Config.WEB_DRIVER, log_path=WEBDRIVER_LOG),
        )

    def projectCheck(self, project, sub_project_name):
        self.sub_project_name = sub_project_name
        if self.skip_existing_check:
            return
        try:
            logger.info("checking for existing project in db")
            try:
                days = int(self.site_data.get('days', 30))
            except (TypeError, ValueError):
                days = 30

            filterdate = datetime.now() - timedelta(days)
            self.projectexist = self.LEAD.find_one(
                {
                    "email": self.lead_data["email"],
                    "project": {
                        "$elemMatch":
                        {
                            "subproject": self.sub_project_name,
                            "applied_time": {"$gte": filterdate},
                            "status": {"$eq": RESULT_SUCCESS},
                        }
                    },
                },
                {"project.$": 1}) is not None

            if self.projectexist:
                self.result = RESULT_SKIPPED
                logger.info("lead already exist")

        except Exception:
            logger.exception("existing-project check failed; registering anyway")
            self.projectexist = False

    def automated_flow(self):
        try:
            if self.projectexist:
                return
            v_automator = project_store.get(self.site_data['name'])
            if v_automator is None:
                raise KeyError("no automation for site '{}'".format(self.site_data['name']))

            self.path = os.path.join(Config.STORAGE_PATH, self.site_data["name"])
            self.path_zoho = os.path.join(Config.STORAGE_PATH, 'zoho')
            os.makedirs(self.path, exist_ok=True)
            os.makedirs(self.path_zoho, exist_ok=True)
            self.automate_path = getsavePath(
                self.path, self.path_zoho, self.site_data['name'], self.sub_project_name,
                self.lead_data.get('name', ''), self.phone)
            self.result = v_automator(
               self.sub_project_name, self.browser, self.site_data, self.lead_data, self.automate_path)
        except Exception as e:
            self.result = RESULT_FAILED
            logger.exception("automte flow error: {}".format(e))

        finally:
            self.upload_data()

    def _upload_screenshot(self, source_index, zoho_copy_index):
        """Upload a screenshot to the Zoho lead, preferring the copy named after the project alias."""
        source = self.automate_path[source_index]
        zoho_copy = self.automate_path[zoho_copy_index]
        try:
            shutil.copy(source, zoho_copy)
            upload_an_attachment(self.lead_id, os.path.abspath(zoho_copy))
        except OSError:
            upload_an_attachment(self.lead_id, os.path.abspath(source))

    def upload_attachments_to_zoho(self):
        if not (self.upload_attachments and self.automate_path):
            return
        if self.result in (RESULT_SUCCESS, RESULT_PARTIAL):
            self._upload_screenshot(0, 3)   # before submitting
            self._upload_screenshot(1, 4)   # after submitting
        if self.result in (RESULT_FAILED, RESULT_PARTIAL):
            self._upload_screenshot(2, 5)   # the error screen
        logger.info("attachments uploaded for lead_id %s", self.lead_id)

    def upload_data(self):
        try:
            self.upload_attachments_to_zoho()
        except Exception:
            logger.exception("attachment upload failed")

        try:
            lead_detail = {
                "projectname": self.site_data['name'],  # akshaya
                "subproject": self.sub_project_name,  # Tango
                "applied_time": getTime(),
                "status": self.result,
                "match_keywords": list(self.match_keywords),
            }
            if self.lead_id:
                lead_detail["lead_id"] = self.lead_id
            dbresult = self.LEAD.update_one(
                {
                    "email": self.lead_data["email"],
                    "phone": self.lead_data["phone"]
                },
                {
                    "$set":
                    {
                        "modified_time": getTime()
                    },
                    "$push":
                    {
                        "project": lead_detail
                    }
                })
            logger.info("lead uploaded")
            return dbresult.upserted_id
        except Exception:
            logger.exception("error occured in automation")
            return -1

    def teardown(self):
        browser = getattr(self, "browser", None)
        if browser is not None:
            try:
                browser.quit()
            except Exception:
                logger.exception("browser did not quit cleanly")
        logger.info("browser quit")
