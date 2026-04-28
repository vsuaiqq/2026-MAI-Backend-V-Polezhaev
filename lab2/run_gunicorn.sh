#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

if [[ ! -x "$ROOT/lab2/.venv/bin/gunicorn" ]]; then
  exit 1
fi

exec "$ROOT/lab2/.venv/bin/gunicorn" \
  -w "${GUNICORN_WORKERS:-2}" \
  -b "${GUNICORN_BIND:-127.0.0.1:8000}" \
  "app.wsgi_app:app" \
  --chdir "$ROOT/lab2"
