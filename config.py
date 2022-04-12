import os
from dotenv import load_dotenv
load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))

required_field = ['name', "phone", "email", "lead_id"]
keyword_field = [
    {
        "field": "project_enquired_for",
        "seperator": ";"
    },
    {
        "field": "interested_project",
        "seperator": ";"
    },
    {
        "field": "interested_localities",
        "seperator": ";"
    }
]


# Dont touch
class Config(object):
    WEB_DRIVER = basedir+"/geckodriver"
    LOG_PATH = basedir+"/logs/"
    DEBUG = False
    TESTING = False
    REDIS_URL = "redis://REDACTED_REDIS_URI"
    BROKER_URL = 'REDACTED'
    RESULT_BACKEND = 'redis://REDACTED_REDIS_URI'
    CELERY_BROKER = "redis://REDACTED_REDIS_URI"
    CELERY_RESULT_BACKEND = "REDACTED"
    FLASK_SENTRY_DSN = "https://redacted@example.com/6320262",
    MONGO_URI = "REDACTED"
    SECRET_KEY = ""
    # CELERY_RESULT_BACKEND = 'REDACTED'


class ProductionConfig(Config):
    ENV = "Production"
    DEBUG = False
    LOG_PATH = basedir+"/logs/"


class DevelopmentConfig(Config):
    ENV = "Development"
    DEBUG = True
    LOG_PATH = basedir+"testing/logs/"


class TestingConfig(Config):
    ENV = "Tesing"
    DEBUG = True
    LOG_PATH = "/var/log/lead_automation/testing/"


class CeleryConfig(Config):
    BROKER_URL = 'REDACTED'
    RESULT_BACKEND = 'redis://REDACTED_REDIS_URI'
    TASK_ROUTES = {
                    "app.tasks.*":
                    {
                        "queue": "lead",
                        "queue": "browser"
                    }
                    # "celery_worker.*":{
                    #     "queue":"lead",
                    #     "queue":"browser"
                    # }
    }


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig
}
