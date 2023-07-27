import os

from app import create_app
from config import Config

if Config.SENTRY_DSN:
    import sentry_sdk
    from sentry_sdk.integrations.flask import FlaskIntegration
    from sentry_sdk.integrations.redis import RedisIntegration
    from sentry_sdk.integrations.celery import CeleryIntegration

    sentry_sdk.init(
        dsn=Config.SENTRY_DSN,
        integrations=[FlaskIntegration(), RedisIntegration(), CeleryIntegration()],
        traces_sample_rate=1.0
    )

app = create_app(os.getenv("FLASK_CONFIG", "production"))

if __name__ == '__main__':
    app.run()
