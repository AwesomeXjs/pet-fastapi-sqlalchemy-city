#!/bin/sh
set -e

sleep 3

alembic upgrade head

gunicorn main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000