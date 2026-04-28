#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [[ ! -x "$ROOT/.venv/bin/gunicorn" ]]; then
  exit 1
fi

exec "$ROOT/.venv/bin/gunicorn" \
  -w "${GUNICORN_WORKERS:-2}" \
  -b "${GUNICORN_BIND:-127.0.0.1:8000}" \
  "headphones_site.wsgi:application" \
  --chdir "$ROOT"
