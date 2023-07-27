FROM python:3.9-slim-bookworm

# Firefox for the Selenium site automations (the web app also uses it for manual retries).
RUN apt-get update \
    && apt-get install -y --no-install-recommends firefox-esr \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /opt/lead_automation

COPY requirements.txt /opt/lead_automation/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . /opt/lead_automation/
RUN chmod +x gunicorn_starter.sh worker_starter.sh geckodriver

ENV LOG_PATH=/opt/lead_automation/logs/ \
    STORAGE_PATH=/opt/lead_automation/storage \
    BROWSER_HEADLESS=true

EXPOSE 5000
ENTRYPOINT [ "./gunicorn_starter.sh" ]
