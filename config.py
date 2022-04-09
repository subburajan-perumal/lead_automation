
import os 
from dotenv import load_dotenv
load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))

#Dont touch 
class Config(object):
    LOG_PATH=basedir+"/logs/"
    DEBUG = False
    TESTING = False
    REDIS_URL = "redis://REDACTED_REDIS_URI"
    BROKER_URL = 'REDACTED'
    RESULT_BACKEND = 'redis://REDACTED_REDIS_URI'
    CELERY_BROKER="redis://REDACTED_REDIS_URI"
    CELERY_RESULT_BACKEND="REDACTED"
   
    MONGO_URI = "REDACTED"
    SECRET_KEY=""
    # CELERY_RESULT_BACKEND = 'REDACTED'

class ProductionConfig(Config):
    ENV = "Production"
    DEBUG = False
    LOG_PATH="/var/log/lead_automation/production/"
class DevelopmentConfig(Config):
    ENV = "Development"
    DEBUG = True
    LOG_PATH="/var/log/lead_automation/Development/"
class TestingConfig(Config):
    ENV="Tesing"
    DEBUG = True
    LOG_PATH="/var/log/lead_automation/testing/"

class CeleryConfig(Config):
    BROKER_URL = 'REDACTED'
    RESULT_BACKEND = 'redis://REDACTED_REDIS_URI'
    TASK_QUEUES={
                    "app.tasks.lead":
                    {   
                        "queue":"lead"
                    }
    }

config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig
}
