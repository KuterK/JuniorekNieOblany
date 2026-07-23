#!/bin/sh
set -eu

if [ "${1:-}" = "web" ]; then
  uv run python manage.py migrate --noinput
  uv run python manage.py collectstatic --noinput
  exec uv run gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 2
fi

if [ "${1:-}" = "worker" ]; then
  exec uv run celery -A config worker --loglevel=info --concurrency=2
fi

exec "$@"
