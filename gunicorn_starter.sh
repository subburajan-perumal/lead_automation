#!/bin/sh
set -e
mkdir -p "${LOG_PATH:-./logs}" "${STORAGE_PATH:-./storage}"
exec gunicorn -c gunicorn.conf.py
