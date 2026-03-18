#!/usr/bin/env sh
set -eu

mkdir -p reports

echo "Waiting for API OpenAPI endpoint..."
until curl -fsS http://localhost:8081/openapi.json >/dev/null 2>&1; do
  sleep 1
done

docker compose run --rm --no-deps --user root zap \
  zap-api-scan.py \
  -t http://api:8081/openapi.json \
  -f openapi \
  -S \
  -D 5 \
  -I \
  -r /zap/wrk/reports/zap-api-openapi-report.html \
  -J /zap/wrk/reports/zap-api-openapi-report.json

echo "Verifying API calls captured in API container logs..."
API_CALLS=$(docker compose logs --no-color api 2>/dev/null | grep -Ec 'GET /openapi.json|GET /api/health|GET /api/accounts|GET /api/customers/|POST /api/transfer' || true)

if [ "$API_CALLS" -eq 0 ]; then
  echo "No API calls detected in api container logs."
  exit 1
fi

echo "Detected $API_CALLS API call log entries."
docker compose logs --no-color api 2>/dev/null | grep -E 'GET /openapi.json|GET /api/health|GET /api/accounts|GET /api/customers/|POST /api/transfer' | tail -n 20

echo "API OpenAPI passive scan completed. Reports in ./reports"
