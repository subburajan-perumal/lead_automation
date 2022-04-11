
from app import create_app
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from sentry_sdk.integrations.redis import RedisIntegration
from sentry_sdk.integrations.celery import CeleryIntegration

sentry_sdk.init(
     dsn="https://redacted@example.com/6320262",
    integrations=[FlaskIntegration(),RedisIntegration(),CeleryIntegration()],
    traces_sample_rate=1.0
    
)

app=create_app("development")

if __name__== '__main__':
    app.run()

# @app.route('/debug-sentry')
# def traces_sampler(sampling_context):
#     # ...
#     # return a number between 0 and 1 or a boolean

#     sentry_sdk.init(
#     dsn="https://redacted@example.com/0",

#     # To set a uniform sample rate
#     traces_sample_rate=0.2,

#     # Alternatively, to control sampling dynamically
#     traces_sampler=traces_sampler
# )

# celery_app=make_celery(app)
# app.run(host="0.0.0.0",port=443,ssl_context=("domain.crt","domain.key"))

# app.run("0.0.0.0")
# app.run("0.0.0.0",8000)
# app.run(debug=True)
# app.run(threaded=True)
# app.run(host="0.0.0.0",port=8686)

