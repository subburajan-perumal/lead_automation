# Real-estate lead automation

Takes property-enquiry leads from Zoho CRM, MagicBricks and 99acres, matches each lead to
builder projects by keyword, and registers it on every matching builder's website with a
Selenium-driven Firefox. Screenshots of each registration are attached back to the Zoho lead.

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for the architecture diagrams and lead flow.

## Stack

| Part | Technology |
| --- | --- |
| Web app | Flask 2.0 on gunicorn 20.1, behind nginx |
| Background jobs | Celery 5.2 with Redis as broker and result backend |
| Database | MongoDB (Atlas) |
| Browser automation | Selenium 4.1, Firefox ESR, geckodriver |
| CRM | Zoho CRM API |
| Error tracking | Sentry (optional) |

Python 3.9.

## Configuration

All settings come from environment variables, read from a `.env` file in the project root.

```sh
cp .env.example .env
```

These must be set, or the app and workers refuse to start:

| Variable | Purpose |
| --- | --- |
| `FLASK_SECRET_KEY` | Flask session signing |
| `MONGO_URI` | MongoDB connection string, including the database name |
| `ZOHO_CLIENT_ID`, `ZOHO_CLIENT_SECRET`, `ZOHO_REFRESH_TOKEN` | Zoho CRM OAuth |

Optional:

| Variable | Purpose |
| --- | --- |
| `MAGICBRICKS_API_KEY` | Enables the hourly MagicBricks sync |
| `ACRES99_USERNAME`, `ACRES99_PASSWORD`, `ACRES99_API_TOKEN` | Enables the hourly 99acres sync |
| `SENTRY_DSN` | Sends errors to Sentry |
| `REDIS_URL` | Redis address (default `redis://localhost:6379/0`) |
| `BROWSER_HEADLESS` | Run Firefox without a window (`true` in Docker) |
| `STORAGE_PATH`, `LOG_PATH` | Where screenshots and logs are written |

`.env` is git-ignored. Never commit it.

## Run with Docker (recommended)

```sh
docker compose up -d --build
```

This starts nginx, the Flask app, Redis, four Celery workers and the Celery scheduler. The app
is served at `http://localhost:8005`.

| Service | Role |
| --- | --- |
| `nginx` | Reverse proxy on port 8005 |
| `flask` | Web app and Zoho webhook |
| `redis` | Task broker and Zoho token cache |
| `lead_worker` | Matches leads to builder projects |
| `browser_worker` | Registers live leads on builder sites |
| `bulk_worker` | Registers leads from CSV uploads |
| `api_worker` | MagicBricks and 99acres sync |
| `beat` | Runs the scheduled jobs |

Useful commands:

```sh
docker compose logs -f browser_worker        # follow one service's logs
docker compose up -d --scale browser_worker=2 # more browser capacity
docker compose down                          # stop everything
```

## Run locally

You need Python 3.9, Redis, and Firefox. The bundled `geckodriver` is a Linux x86-64 binary;
on other platforms install geckodriver yourself and set `WEB_DRIVER` to its path.

```sh
python3.9 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # then fill it in
```

Start each process in its own terminal:

```sh
./gunicorn_starter.sh             # web app on :5000
./worker_starter.sh lead          # lead matching, Zoho token refresh, cleanup
./worker_starter.sh browser       # live site registrations
./worker_starter.sh bulk          # CSV upload registrations
./worker_starter.sh api           # MagicBricks and 99acres sync
./worker_starter.sh beat          # scheduler
```

To receive Zoho webhooks on a local machine, expose port 5000 with a tunnel such as ngrok.

## Endpoints

| Route | Use |
| --- | --- |
| `POST /` | Zoho CRM webhook. Needs `name`, `phone`, `email`, `lead_id` |
| `POST /retry_leads` | Re-queue one lead for one sub-project |
| `GET /tasks/<task_id>` | Celery task status |
| `/bulk_upload`, `/bulk_leads_list` | Upload a CSV of leads and list past uploads |
| `/lead/all`, `/lead/today` | Lead history |
| `/lead/error_retry` | Re-run one failed site registration |
| `/site/`, `/site/add`, `/site/<name>` | Manage builder sites, projects and keywords |

## Scheduled jobs

| Job | When |
| --- | --- |
| MagicBricks sync | Every hour |
| 99acres sync | Every hour |
| Zoho access token refresh | Every 30 minutes |
| Delete screenshots older than 200 days | Daily at 23:00 |

## Monitoring

Run Flower to see workers, queues and task history:

```sh
celery -A app.tasks flower   # http://localhost:5555
```

Check one task from the web app with `GET /tasks/<task_id>`.

Logs go to `LOG_PATH` (`./logs` by default). Set `SENTRY_DSN` to send errors from Flask,
Celery and Redis to Sentry.

## Adding a builder site

1. Write the form-filling function in `app/functions/browser_automation.py`.
2. Register it by site name in `project_store` in `app/functions/site_base.py`.
3. Add the site, its projects and their match keywords at `/site/add`.

## Project layout

```text
app/
  __init__.py          Flask app factory
  tasks.py             Celery app, queues, schedule and tasks
  views/               Flask blueprints: home, lead, site, error pages
  functions/           Lead matching and per-site Selenium automation
  util/                Zoho API, webhook parsing, helpers
  templates/, static/  Admin pages
config.py              Settings, read from the environment
docs/ARCHITECTURE.md   Architecture diagrams
nginx/                 Reverse proxy image
test/                  Manual test scripts
```
