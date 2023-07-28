# Architecture

Real-estate lead automation takes property-enquiry leads from Zoho CRM (and from the
MagicBricks and 99acres APIs), matches each lead to builder projects by keyword, and
registers the lead on every matching builder's website with a Selenium-driven Firefox.
Screenshots of each registration are attached back to the Zoho lead.

This page starts with one overview diagram, then shows each part on its own:

1. [Overview](#1-overview)
2. [Web layer](#2-web-layer)
3. [Task queues and workers](#3-task-queues-and-workers)
4. [Lead pipeline](#4-lead-pipeline)
5. [Site automation](#5-site-automation)
6. [Scheduled jobs and portal sync](#6-scheduled-jobs-and-portal-sync)
7. [Data stores](#7-data-stores)

## 1. Overview

```mermaid
flowchart LR
    sources(["Lead sources<br/>Zoho webhook · operators · CSV upload"])
    web["Web layer<br/>nginx + Flask"]
    queue[("Task queue<br/>Redis + Celery")]
    workers["Workers<br/>lead · browser · bulk · api · beat"]
    data[("Data<br/>MongoDB · screenshot storage")]
    external["External systems<br/>Zoho CRM · builder websites<br/>MagicBricks · 99acres"]

    sources --> web
    web -- "queue tasks" --> queue
    queue --> workers
    web <--> data
    workers <--> data
    workers <--> external
```

| Part | What it does | Details |
| --- | --- | --- |
| Web layer | Receives webhooks, serves the admin pages, queues work | [§2](#2-web-layer) |
| Task queues and workers | Runs every job in the background, split by queue | [§3](#3-task-queues-and-workers) |
| Lead pipeline | Turns one lead into one registration per matching project | [§4](#4-lead-pipeline) |
| Site automation | Fills one builder's enquiry form and records the result | [§5](#5-site-automation) |
| Scheduled jobs | Pulls portal leads, refreshes the Zoho token, cleans up | [§6](#6-scheduled-jobs-and-portal-sync) |
| Data stores | What is kept where, and who reads or writes it | [§7](#7-data-stores) |

Everything runs from `docker-compose.yml` except MongoDB, which is external (Atlas) and set by
`MONGO_URI`. All settings come from `.env`; see `.env.example` and `config.py`.

## 2. Web layer

nginx listens on host port 8005 and proxies to gunicorn (`run:app`, one `gthread` worker with
three threads, 600 s timeout). The Flask app is built in `app/__init__.py` from four blueprints.

```mermaid
flowchart LR
    zoho(["Zoho CRM webhook"])
    user(["Operator"])
    nginx["nginx<br/>:8005 → flask:5000"]

    subgraph flask["Flask app (gunicorn)"]
        direction TB
        home["home · app/views/home.py<br/>POST /  ·  POST /retry_leads<br/>/bulk_upload  ·  /bulk_leads_list<br/>GET /tasks/&lt;task_id&gt;"]
        lead["lead · app/views/lead.py<br/>/lead/all  ·  /lead/today<br/>/lead/error_retry"]
        site["site · app/views/site.py<br/>/site/  ·  /site/add  ·  /site/&lt;name&gt;"]
        err["errorHandler<br/>404 · 405 pages"]
    end

    redis[("Redis")]
    mongo[("MongoDB")]
    firefox["Firefox<br/>(in the flask container)"]

    zoho --> nginx
    user --> nginx
    nginx --> home & lead & site

    home -- "lead → queue lead<br/>bulk_lead → queue bulk" --> redis
    home -- "task status" --> redis
    home -- "bulk_leads" --> mongo
    lead -- "read leads, Site" --> mongo
    lead -- "error retry runs<br/>synchronously" --> firefox
    site -- "read / add Site" --> mongo
```

- **`POST /`**: the Zoho webhook. `find_format()` reads JSON or form bodies and needs
  `name`, `phone`, `email` and `lead_id`. Valid leads go to the `lead` task.
- **`POST /retry_leads`**: re-queues one lead for one sub-project (`source: retry`).
- **`/bulk_upload`**: stores CSV rows in `bulk_leads` and queues each one as `bulk_lead`.
- **`/lead/error_retry`**: re-runs one site registration inside the web request, without
  Celery, using `error_site_base.SiteAutomator1`.

## 3. Task queues and workers

Every Celery process uses the same app (`app.tasks`). Routing is set in `task_routes` in
`app/tasks.py`, and each worker is started by `worker_starter.sh <role>`.

```mermaid
flowchart LR
    subgraph producers["Producers"]
        direction TB
        flask["Flask"]
        beat["beat<br/>scheduler"]
        lead_task["lead / bulk_lead<br/>(fan-out)"]
    end

    subgraph redis["Redis queues"]
        direction TB
        q_lead[["lead · default · celery"]]
        q_browser[["browser"]]
        q_bulk[["bulk"]]
        q_api[["api_lead"]]
    end

    subgraph workers["Workers"]
        direction TB
        w_lead["lead_worker · c=1<br/>lead · save_access_token<br/>removing_older_img"]
        w_browser["browser_worker · c=2<br/>browserAutomate"]
        w_bulk["bulk_worker · c=2<br/>bulk_lead · browserAutomateBulk"]
        w_api["api_worker · c=1<br/>run_magicbricks_api<br/>run_99acres_api"]
    end

    flask --> q_lead & q_bulk
    beat --> q_lead & q_api
    lead_task --> q_browser & q_bulk

    q_lead --> w_lead
    q_browser --> w_browser
    q_bulk --> w_bulk
    q_api --> w_api
```

| Worker | Queues | Concurrency | Firefox |
| --- | --- | --- | --- |
| `lead_worker` | `default`, `lead`, `celery` | 1 | no |
| `browser_worker` | `browser` | `BROWSER_CONCURRENCY` (default 2) | yes, 1 GB shm |
| `bulk_worker` | `bulk` | 2 | yes, 1 GB shm |
| `api_worker` | `api_lead` | 1 | no |
| `beat` | (sends only) | n/a | no |

Bulk leads stay on the `bulk` queue from start to finish, so a large CSV upload doesn't
hold up live Zoho leads on the `browser` queue.

## 4. Lead pipeline

One webhook becomes one browser task for every builder project whose keywords match the lead.

```mermaid
sequenceDiagram
    autonumber
    participant Z as Zoho CRM
    participant F as Flask (POST /)
    participant R as Redis
    participant L as lead_worker
    participant M as MongoDB
    participant B as browser_worker

    Z->>F: webhook with name, phone, email, lead_id
    F->>F: find_format() checks required fields
    F->>R: lead task on "lead" queue
    F-->>Z: 200 "received"
    R->>L: lead(**lead_data)
    L->>L: normalise phone and email
    L->>M: create lead in "leads" if new
    L->>L: collect keywords from project_enquired_for,<br/>interested_properties, interested_localities, ...
    L->>M: find active Site projects with a matching keyword
    L->>R: group of browserAutomate(site, lead),<br/>one per matched project
    R->>B: browserAutomate(site, lead)
    Note over B: continues in §5 Site automation
```

`bulk_lead` does the same with `browserAutomateBulk` on the `bulk` queue. A lead with no
keywords is matched against the `None (default)` keyword instead.

## 5. Site automation

`SiteAutomator` in `app/functions/site_base.py` handles one lead for one builder project. The
form-filling code for each builder lives in `app/functions/browser_automation.py` and is looked
up by site name in `project_store`.

```mermaid
flowchart TD
    start(["browserAutomate(site, lead)"])
    match{"Lead keywords match<br/>this project?"}
    none(["Return: no matched keywords"])
    open["Start Firefox<br/>(SiteAutomator)"]
    check{"Registered successfully<br/>within the site's window<br/>(default 30 days)?"}
    lookup["Find the site's function<br/>in project_store"]
    run["Fill and submit<br/>the enquiry form"]
    shots[/"Screenshots in storage:<br/>before · after · error"/]
    upload["Attach screenshots<br/>to the Zoho lead"]
    record[("Push {subproject, status,<br/>applied_time} onto the lead<br/>in MongoDB")]
    quit(["Quit Firefox"])

    start --> match
    match -- no --> none
    match -- yes --> open --> check
    check -- "yes: SKIPPED" --> record
    check -- no --> lookup --> run --> shots
    shots -- "SUCCESS · PARTIAL · FAILED" --> upload --> record
    record --> quit
```

| Status | Value | Meaning | Screenshots attached |
| --- | --- | --- | --- |
| `SKIPPED` | 0 | Already registered with this project inside the window | none |
| `SUCCESS` | 1 | Form submitted | before, after |
| `PARTIAL` | -1 | Submitted, but the site also showed an error | before, after, error |
| `FAILED` | 2 | The automation raised an error, or the site has no function | error, if one was taken |

Firefox is always closed in a `finally`, so a failing site doesn't leave a browser process
running on the worker.

## 6. Scheduled jobs and portal sync

`beat` sends these tasks on the schedule in `beat_schedule` (`app/tasks.py`).

```mermaid
flowchart LR
    beat["beat"]

    subgraph api_worker["api_worker"]
        mb["run_magicbricks_api<br/>hourly"]
        acres["run_99acres_api<br/>hourly"]
    end

    subgraph lead_worker["lead_worker"]
        token["save_access_token<br/>every 30 min"]
        clean["removing_older_img<br/>daily 23:00"]
    end

    magicbricks["MagicBricks<br/>rating API"]
    acres99["99acres<br/>response API"]
    api_leads[("MongoDB<br/>API_leads")]
    zoho["Zoho CRM<br/>Deals search · Leads upsert"]
    zoho_oauth["Zoho OAuth"]
    redis[("Redis<br/>token cache")]
    storage[/"storage volume"/]

    beat --> mb & acres & token & clean

    mb -- "recent leads" --> magicbricks
    acres -- "responses from the last day" --> acres99
    mb & acres -- "skip if synced in the last day" --> api_leads
    mb & acres -- "look up project, upsert lead" --> zoho

    token -- "refresh" --> zoho_oauth
    token -- "store access token" --> redis
    clean -- "delete screenshots<br/>older than 200 days" --> storage
```

Every Zoho call reads the cached access token from Redis first and only asks Zoho OAuth for a
new one if the cache is empty.

## 7. Data stores

```mermaid
flowchart LR
    subgraph components["Components"]
        direction TB
        flask["Flask"]
        lead_w["lead / bulk_lead"]
        site_auto["Site automation"]
        api_w["Portal sync"]
        token["save_access_token"]
        clean["removing_older_img"]
    end

    subgraph mongo["MongoDB (MONGO_DB_NAME)"]
        direction TB
        Site[("Site<br/>builders, projects, keywords")]
        leads[("leads<br/>one per person + project results")]
        bulk_leads[("bulk_leads<br/>uploaded CSV rows")]
        API_leads[("API_leads<br/>portal sync log")]
    end

    subgraph redis_box["Redis"]
        direction TB
        broker[("Celery broker + results")]
        zoho_token[("lead_automation:zoho_access_token")]
    end

    storage[/"storage volume<br/>screenshots per site + zoho copies"/]

    flask -- "read, add" --> Site
    flask -- read --> leads
    flask -- "write, read" --> bulk_leads
    flask -- "send tasks, read status" --> broker
    lead_w -- read --> Site
    lead_w -- "create lead" --> leads
    site_auto -- "check window, push result" --> leads
    site_auto -- write --> storage
    site_auto & api_w -- read --> zoho_token
    api_w -- "upsert, dedupe" --> API_leads
    token -- write --> zoho_token
    clean -- delete --> storage
```

| Store | Contents | Written by | Read by |
| --- | --- | --- | --- |
| `Site` | Builder sites, their projects and match keywords, active status | `/site/add` | lead matching, admin pages, error retry |
| `leads` | One document per email and phone, with a `project` list of registration results | `lead`, `bulk_lead`, site automation | `/lead/*` pages, window check, error retry |
| `bulk_leads` | Rows from CSV uploads | `/bulk_upload` | `/bulk_leads_list` |
| `API_leads` | Leads already sent from MagicBricks and 99acres | portal sync | portal sync |
| Redis | Celery messages and results; cached Zoho access token | Celery, Zoho token refresh | workers, `/tasks/<id>`, Zoho calls |
| `storage` volume | Screenshots, grouped by site, with copies for Zoho | site automation | Zoho upload, cleanup |
