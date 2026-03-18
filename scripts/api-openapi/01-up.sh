#!/usr/bin/env sh
set -eu

docker compose up -d --build api

echo "Waiting for API OpenAPI endpoint..."
until curl -fsS http://localhost:8081/openapi.json >/dev/null 2>&1; do
  sleep 1
done

echo "API playground started on http://localhost:8081"
