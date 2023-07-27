#!/bin/sh
# Starts one Celery process. Usage: worker_starter.sh <lead|browser|bulk|api|beat>
set -e
mkdir -p "${LOG_PATH:-./logs}" "${STORAGE_PATH:-./storage}"
case "$1" in
  lead)    exec celery -A app.tasks worker -l info -c 1 -Q default,lead,celery -n leadworker@%h ;;
  browser) exec celery -A app.tasks worker -l info -c "${BROWSER_CONCURRENCY:-2}" -Q browser -n selenium_worker@%h ;;
  bulk)    exec celery -A app.tasks worker -l info -c 2 -Q bulk -n bulk_leads@%h ;;
  api)     exec celery -A app.tasks worker -l info -c 1 -Q api_lead -n api_leads@%h ;;
  beat)    exec celery -A app.tasks beat -l info -s "${LOG_PATH:-./logs}/celerybeat-schedule" ;;
  *)       echo "usage: $0 <lead|browser|bulk|api|beat>" >&2; exit 2 ;;
esac
