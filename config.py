import os
from dotenv import load_dotenv
load_dotenv()


basedir = os.path.abspath(os.path.dirname(__file__))


def env(name, default=None):
    """Read a setting from the environment, treating empty strings as unset."""
    value = os.getenv(name)
    return value if value not in (None, "") else default


def env_list(name, default=""):
    return [item.strip() for item in env(name, default).split(",") if item.strip()]


def env_bool(name, default=False):
    value = env(name)
    if value is None:
        return default
    return value.strip().lower() in ("1", "true", "yes", "on")


required_field = ['name', "phone", "email", "lead_id"]
keyword_field = [
    {
        "field": "project_enquired_for",
        "seperator": ";"
    },
    {
        "field": "interested_properties",
        "seperator": ";"
    },
    {
        "field": "interested_localities",
        "seperator": ";"
    },
    {
        "field": "initial_enquiry_particulars_automation",
        "seperator": ";"
    }
]
phone_field = ["phone", "mobile", "alt_phone"]


class Config(object):
    WEB_DRIVER = env("WEB_DRIVER", basedir + "/geckodriver")
    LOG_PATH = env("LOG_PATH", basedir + "/logs/")
    STORAGE_PATH = env("STORAGE_PATH", "./storage")
    DEBUG = False
    TESTING = False

    SECRET_KEY = env("FLASK_SECRET_KEY")
    SENTRY_DSN = env("SENTRY_DSN")
    APP_BASE_URL = env("APP_BASE_URL", "")

    # MONGO_URI must include the database name, e.g. mongodb+srv://user:pass@host/lead_automation
    MONGO_URI = env("MONGO_URI")
    MONGO_DB_NAME = env("MONGO_DB_NAME", "lead_automation")

    REDIS_URL = env("REDIS_URL", "redis://localhost:6379/0")
    BROKER_URL = env("CELERY_BROKER_URL", REDIS_URL)
    RESULT_BACKEND = env("CELERY_RESULT_BACKEND", REDIS_URL)
    CELERY_BROKER = BROKER_URL
    CELERY_RESULT_BACKEND = RESULT_BACKEND

    ZOHO_CLIENT_ID = env("ZOHO_CLIENT_ID")
    ZOHO_CLIENT_SECRET = env("ZOHO_CLIENT_SECRET")
    ZOHO_REFRESH_TOKEN = env("ZOHO_REFRESH_TOKEN")
    ZOHO_ACCOUNTS_URL = env("ZOHO_ACCOUNTS_URL", "https://accounts.zoho.com")
    ZOHO_API_URL = env("ZOHO_API_URL", "https://www.zohoapis.com")

    MAILGUN_API_KEY = env("MAILGUN_API_KEY")
    MAILGUN_DOMAIN = env("MAILGUN_DOMAIN")
    MAILGUN_TO = env_list("MAILGUN_TO")

    MAGICBRICKS_API_KEY = env("MAGICBRICKS_API_KEY")
    ACRES99_USERNAME = env("ACRES99_USERNAME")
    ACRES99_PASSWORD = env("ACRES99_PASSWORD")
    ACRES99_API_TOKEN = env("ACRES99_API_TOKEN")

    BROWSER_HEADLESS = env_bool("BROWSER_HEADLESS", False)

    # Settings without which the web app or the lead workers cannot do their job.
    REQUIRED_SETTINGS = (
        "SECRET_KEY",
        "MONGO_URI",
        "ZOHO_CLIENT_ID",
        "ZOHO_CLIENT_SECRET",
        "ZOHO_REFRESH_TOKEN",
    )

    @classmethod
    def missing_settings(cls):
        return [name for name in cls.REQUIRED_SETTINGS if not getattr(cls, name)]

    @classmethod
    def validate(cls):
        missing = cls.missing_settings()
        if missing:
            raise RuntimeError(
                "Missing required settings: {}. Copy .env.example to .env and fill them in.".format(
                    ", ".join(missing)
                )
            )


class ProductionConfig(Config):
    ENV = "Production"
    DEBUG = False


class DevelopmentConfig(Config):
    ENV = "Development"
    DEBUG = True


class TestingConfig(Config):
    ENV = "Testing"
    DEBUG = True
    TESTING = True


class CeleryConfig(Config):
    TASK_ROUTES = {
                    "app.tasks.*":
                    {
                        "queue": "lead,celery"
                    }
    }


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
}
