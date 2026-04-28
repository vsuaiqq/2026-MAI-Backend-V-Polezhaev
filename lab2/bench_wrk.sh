set -euo pipefail

if ! command -v wrk >/dev/null 2>&1; then
  exit 1
fi

BASE_PUBLIC="${BASE_PUBLIC:-http://127.0.0.1:8080/public/test.txt}"
BASE_GUNICORN="${BASE_GUNICORN:-http://127.0.0.1:8080/gunicorn/password}"
BASE_DIRECT="${BASE_DIRECT:-http://127.0.0.1:8000/password}"

DURATION="${DURATION:-10s}"
THREADS="${THREADS:-2}"

echo "== 1) nginx public =="
wrk -t"$THREADS" -c50 -d"$DURATION" "$BASE_PUBLIC"
echo

echo "== 2) nginx -> gunicorn (upstream) =="
wrk -t"$THREADS" -c50 -d"$DURATION" "$BASE_GUNICORN"
echo

echo "== 3) direct gunicorn =="
wrk -t"$THREADS" -c50 -d"$DURATION" "$BASE_DIRECT"
echo

