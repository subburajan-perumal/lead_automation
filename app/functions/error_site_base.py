from app.functions.site_base import SiteAutomator
from config import env_bool


class SiteAutomator1(SiteAutomator):
    """Manual retry of a failed registration from the /lead/error_retry page.

    The operator picks the project, so the keyword match and the "already registered"
    check are skipped, and the Zoho lead id comes from the form.
    """

    skip_existing_check = True
    # Runs inside the web process, which has no display, so headless unless told otherwise.
    headless = env_bool("BROWSER_HEADLESS", True)

    def __init__(self, phone, email, lead_data, match_keywords, site_data, sub_project_name, lead_id) -> None:
        super().__init__(phone, email, lead_data, match_keywords, site_data, lead_id=lead_id)
        self.sub_project_name = sub_project_name
