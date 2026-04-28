#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

exec "$ROOT/.venv/bin/python" "$ROOT/manage.py" runserver "${RUN_BIND:-127.0.0.1:8000}"
