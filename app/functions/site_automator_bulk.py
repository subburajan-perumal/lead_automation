from app.functions.site_base import SiteAutomator as BaseSiteAutomator


class SiteAutomator(BaseSiteAutomator):
    """Bulk CSV leads: same site flow, but screenshots stay local instead of going to Zoho."""

    upload_attachments = False
