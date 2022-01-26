class Config(object):
    DEBUG = False
    TESTING = False
    broker_url = 'redis://REDACTED_REDIS_URI'
    result_backend= 'redis://REDACTED_REDIS_URI'
    REDIS_URL="redis://REDACTED_REDIS_URI"
    MONGO_URI="REDACTED"
    
    # CELERY_RESULT_BACKEND = 'REDACTED'

class ProductionConfig(Config):
    ENV="Production"

class DevelopmentConfig(Config):
    ENV="Development"
    DEBUG = True

class TestingConfig(Config):
    ENV="Tesing"
    TESTING = True