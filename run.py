from app import create_app
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from sentry_sdk.integrations.redis import RedisIntegration
from sentry_sdk.integrations.celery import CeleryIntegration

sentry_sdk.init(
    dsn="https://redacted@example.com/6320262",
    integrations=[FlaskIntegration(), RedisIntegration(), CeleryIntegration()],
    traces_sample_rate=1.0
)

app = create_app("development")

if __name__ == '__main__':
    app.run()

