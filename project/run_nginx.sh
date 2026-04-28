#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if ! command -v nginx >/dev/null 2>&1; then
  exit 1
fi

exec nginx -c nginx.conf -p "$ROOT"
